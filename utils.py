from sys import platform
from screeninfo import get_monitors, Monitor


def detect_os():
    if platform == "linux" or platform == "linux2":
        return 'linux'
    elif platform == "darwin":
        return 'OS X'
    elif platform == "win32":
        return 'Windows'


def get_monitors_info() -> list:
    result = []
    for monitor in get_monitors():
        result.append(monitor)
    return result


def get_monitor_resolution() -> tuple:
    for monitor in get_monitors_info():
        if monitor.is_primary:
            return monitor.width, monitor.height
    return ()


def main():
    print(get_monitor_resolution())


if __name__ == '__main__':
    main()