import json
import re
from enum import Enum
from http.client import HTTPResponse
from sys import stderr, stdout
from time import sleep, time
from typing import Dict
from urllib.request import Request, urlopen

CONFIG = {
    "name": "ipaddress",
    "author": "Bohan Wang <wbhan_cn@qq.com>",
    "timeout": 3.0,
    "pattern": r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
    "maxThreads": 10,
    "urls": [
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

    # FIXME: 完成GET方法
    def get(self) -> str:
        if self._type == ReturnType.STRING:
            return req(self._url)
        elif self._type == ReturnType.LSTRING:
            res = re.findall(CONFIG["pattern"], req(self._url))
            if len(res) > 0:
                return res[0]
            else:
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


def get_my_ip(type: IPType):
    if type == IPType.WAN:
        typeMap = {
            "string", ReturnType.STRING,
            "lstring", ReturnType.LSTRING,
            "json", ReturnType.JSON
        }
        providers = []
        for url in CONFIG["urls"]:
            if url["type"] == "json":
                p = IPProvider(url["url"], typeMap[url["type"]], url["field"])
            else:
                p = IPProvider(url["url"], typeMap[url["type"]])
            providers.append(p)

        # FIXME: 对providers进行筛选
        
    elif type == IPType.LAN:
        pass


if __name__ == '__main__':
    # resp = req("http://ip.42.pl/raw", CONFIG["header"], CONFIG["timeout"])

    # pd = IPProvider("http://ip.42.pl/raw", ReturnType.STRING)
    # print(pd.get())

    r1 = IPProvider("http://ip.42.pl/raw", ReturnType.STRING)
    r2 = IPProvider("http://httpbin.org/ip", ReturnType.JSON, field="origin")
    r3 = IPProvider("http://checkip.dyndns.com/", ReturnType.LSTRING)
    print(r1.get())
    print(r2.get())
    print(r3.get())
