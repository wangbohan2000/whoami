from asyncio import futures
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import as_completed
import json
from multiprocessing import pool
from queue import Queue
import re
from enum import Enum
from http.client import HTTPResponse
import socket
from sys import stderr, stdout
from time import sleep, time
from typing import Dict, List, Tuple
from urllib.request import Request, urlopen

from tqdm.contrib import concurrent

CONFIG = {
    "name": "ipaddress",
    "author": "Bohan Wang <wbhan_cn@qq.com>",
    "timeout": 1,
    "pattern": r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
    "maxThreads": 10,
    "urls": [
        {
            "url": "http://139.155.43.138:10240/",
            "returnType": "string"
        },
        {
            "url": "http://ip.42.pl/raw",
            "returnType": "string"
        },
        {
            "url": "http://jsonip.com",
            "returnType": "json",
            "field": "ip"
        },
        {
            "url": "http://httpbin.org/ip",
            "returnType": "json",
            "field": "origin"
        },
        {
            "url": "http://whatismyip.akamai.com/",
            "returnType": "string"
        },
        {
            "url": "http://icanhazip.com/",
            "returnType": "string"
        },
        {
            "url": "members.3322.org/dyndns/getip",
            "returnType": "string"
        },
        {
            "url": "http://checkip.dyndns.com/",
            "returnType": "lstring"
        },
        {
            "url": "http://pv.sohu.com/cityjson",
            "returnType": "lstring"
        },
        {
            "url": "https://ifconfig.me/",
            "returnType": "string"
        }
    ],
    "header": {
        "Connection": "keep-alive",
        "DNT": 1,
        "Upgrade-Insecure-Requests": 1,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,zh-HK;q=0.8"
    }
}


class ReturnType(Enum):
    STRING = "string",
    LSTRING = "lstring",
    JSON = "json",


class IPType(Enum):
    WAN = 0,
    LAN = 1,


class IPProvider(object):
    def __init__(self, url: str, type: ReturnType, field: str = None) -> None:
        self._url = url
        self._type = type
        self._field = field

    def get(self) -> str:
        if self._type == ReturnType.STRING:
            return req(self._url)
        elif self._type == ReturnType.LSTRING:
            try:
                res = re.findall(CONFIG["pattern"], req(self._url))
                if len(res) > 0:
                    return res[0]
                else:
                    return None
            except TypeError:
                return None
        elif self._type == ReturnType.JSON:
            if self._field is None:
                raise Exception("Must have a field to parse json!")
            try:
                content = req(self._url)
                res = json.loads(content)
                return res[self._field]
            except:
                return None


def req(url: str,
        header: Dict = CONFIG["header"],
        timeout: float = CONFIG["timeout"],
        method: str = "GET",
        encoding: str = "utf8") -> str:
    try:
        r = Request(url, headers=header, method=method)
        resp = urlopen(r, timeout=timeout)
        ip = resp.read().decode(encoding).strip()
        resp.close()
        return ip
    except Exception:
        return None


def choice(providers: List[IPProvider]) -> str:
    pool = ThreadPoolExecutor(max_workers=len(providers))
    futures = [pool.submit(provider.get) for provider in providers]
    for i in as_completed(futures):
        now = i.result()
        if now is not None:
            return now


def get_my_ip(type: IPType) -> List[str]:
    if type == IPType.WAN:
        typeMap = {
            "string": ReturnType.STRING,
            "lstring": ReturnType.LSTRING,
            "json": ReturnType.JSON
        }
        providers = []
        for url in CONFIG["urls"]:
            if url["returnType"] == "json":
                p = IPProvider(
                    url["url"], typeMap[url["returnType"]], url["field"])
            else:
                p = IPProvider(url["url"], typeMap[url["returnType"]])
            providers.append(p)
        return [choice(providers=providers)]
    elif type == IPType.LAN:
        try:
            hostname = socket.gethostname()
            addrs = socket.getaddrinfo(hostname, None)
            return [info[4][0] for info in addrs]
        except:
            return ["127.0.0.1"]


if __name__ == '__main__':
    print(get_my_ip(IPType.LAN))
