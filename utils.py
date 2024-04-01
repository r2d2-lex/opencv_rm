# import psutil
import subprocess

from sys import platform
from screeninfo import get_monitors, Monitor
from config import XDT_TOOL_INFO

WINDOWS_PLATFORM = 'windows'
LINUX_PLATFORM = 'linux'


def start_shell_command(cmd: str) -> str:
    try:
        result = subprocess.run(cmd.split(), stdout=subprocess.PIPE, text=True)
        return result.stdout
    except (AttributeError, FileNotFoundError, OSError, PermissionError, IndexError) as err:
        print(f'Error running command: {cmd}\r\nDetails: {err}')
    return ''


def get_active_window_title(os):
    active_window_name = None
    if os == WINDOWS_PLATFORM:
        try:
            pass
            # active_window_name = psutil.Process(
            #     win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())[1]).name()
        except Exception:
            pass
    elif os == LINUX_PLATFORM:
        try:
            active_window_name = start_shell_command(XDT_TOOL_INFO)
        except Exception:
            pass
    if active_window_name:
        active_window_name = active_window_name.strip()
    return active_window_name


def detect_os():
    if platform == "linux" or platform == "linux2":
        return LINUX_PLATFORM
    elif platform == "darwin":
        return 'OS X'
    elif platform == "win32":
        return WINDOWS_PLATFORM


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
    print(detect_os())


if __name__ == '__main__':
    main()