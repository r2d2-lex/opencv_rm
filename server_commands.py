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
    pyautogui.PAUSE = 1
    pyautogui.FAILSAFE = True
    cmd = ''
    arg1 = ''
    arg2 = ''

    command = command.split()

    try:
        index = 0
        for arg in command:
            print(f'Index {index} arg: {arg}')
            if index == 0:
                cmd = str(arg)
            elif index == 1:
                arg1 = int(arg)
            elif index == 2:
                arg2 = int(arg)
            index += 1

        if cmd == EVENT_MOUSEMOVE:
            pyautogui.moveTo(arg1, arg2)

        if cmd == EVENT_LBUTTONDBLCLK:
            pyautogui.doubleClick(arg1, arg2)

        elif cmd == EVENT_LBUTTONDOWN:
            pyautogui.leftClick(arg1, arg2)

        elif cmd == EVENT_RBUTTONDOWN:
            pyautogui.rightClick(arg1, arg2)

        else:
            print(f'Other command {cmd}')

    except (IndexError, ValueError) as error:
        print(f'Unknown command: {command} - {error}')

    print('\r\n')
    return
