from asyncio.tasks import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from time import sleep


def task(x):
    sleep(x)
    return x


def choice():
    pool = ThreadPoolExecutor(max_workers=10)
    futures = [pool.submit(task, i) for i in range(10)]

    while 1:
        for future in futures:
            if future.done():
                return future.result()


if __name__ == '__main__':
    print(choice())