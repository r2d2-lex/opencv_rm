import pyautogui

QUIT_COMMAND = 'quit'
EVENT_LBUTTONDBLCLK = 'EVENT_LBUTTONDBLCLK'
EVENT_LBUTTONDOWN = 'EVENT_LBUTTONDOWN'
EVENT_RBUTTONDOWN = 'EVENT_RBUTTONDOWN'
EVENT_MOUSEMOVE = 'EVENT_MOUSEMOVE'


def start_command(command):
    if command == EVENT_MOUSEMOVE:
        pass
        # pyautogui.move(mouse_x, mouse_y)

    if command == EVENT_LBUTTONDBLCLK:
        pyautogui.doubleClick()

    elif command == EVENT_LBUTTONDOWN:
        pass

    elif command == EVENT_RBUTTONDOWN:
        pass

    else:
        print(f'Other command {command}')
