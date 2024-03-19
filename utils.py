from sys import platform


def detect_os():
    if platform == "linux" or platform == "linux2":
        return 'linux'
    elif platform == "darwin":
        return 'OS X'
    elif platform == "win32":
        return 'Windows'


def main():
    print(detect_os())


if __name__ == '__main__':
    main()