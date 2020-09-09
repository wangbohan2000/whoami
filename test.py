from threading import Thread


def p(x):
    while 1:
        print(x)


if __name__ == '__main__':
    Thread(target=p(1)).start()
    Thread(target=p(2)).start()
