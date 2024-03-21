import pyautogui

QUIT_COMMAND = 'quit'
EVENT_LBUTTONDBLCLK = 'EVENT_LBUTTONDBLCLK'
EVENT_LBUTTONDOWN = 'EVENT_LBUTTONDOWN'
EVENT_RBUTTONDOWN = 'EVENT_RBUTTONDOWN'
EVENT_MOUSEMOVE = 'EVENT_MOUSEMOVE'
COMMAND = 0
ARG1 = 1
ARG2 = 2
ARG3 = 3


def start_command(command):
    command = command.split()

    index = 0
    for arg in command:
        print(f'Index {index} arg: {arg}')
        index += 1

    try:
        cmd = command[COMMAND]
        if cmd == EVENT_MOUSEMOVE:
            pyautogui.move(command[ARG1], command[ARG2])

        if cmd == EVENT_LBUTTONDBLCLK:
            pyautogui.doubleClick(command[ARG1], command[ARG2])

        elif cmd == EVENT_LBUTTONDOWN:
            pyautogui.leftClick(command[ARG1], command[ARG2])

        elif cmd == EVENT_RBUTTONDOWN:
            pyautogui.rightClick(command[ARG1], command[ARG2])

        else:
            print(f'Other command {cmd}')

    except IndexError as error:
        print(f'Unknown command: {command} - {error}')

    print('\r\n')
    return
