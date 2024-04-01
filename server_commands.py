import pyautogui

QUIT_COMMAND = 'quit'
EVENT_LBUTTONDBLCLK = 'EVENT_LBUTTONDBLCLK'
EVENT_LBUTTONDOWN = 'EVENT_LBUTTONDOWN'
EVENT_RBUTTONDOWN = 'EVENT_RBUTTONDOWN'
EVENT_MOUSEMOVE = 'EVENT_MOUSEMOVE'
EVENT_KB_KEY = 'EVENT_KEYBOARD'
MOUSE_EVENTS = [
    EVENT_LBUTTONDBLCLK,
    EVENT_LBUTTONDOWN,
    EVENT_RBUTTONDOWN,
    EVENT_MOUSEMOVE,
]

KEY_CTRL = 'Key.ctrl'
KEY_SHIFT = 'Key.shift'
KEY_TAB = 'Key.tab'
KEY_ESCAPE = 'Key.esc'
KEY_CAPS_LOCK = 'Key.caps_lock'
KEY_ENTER = 'Key.enter'
KEY_SHIFT_R = 'Key.shift_r'
KEY_CTRL_R = 'Key.ctrl_r'
KEY_BACKSPACE = 'Key.backspace'
KEY_ALT_R = 'Key.alt_r'
KEY_ALT = 'Key.alt'

KB_ACTIONS = {
    KEY_CTRL: 'ctrl',
    KEY_SHIFT: 'shift',
    KEY_TAB: 'tab',
    KEY_ESCAPE: 'esc',
    KEY_CAPS_LOCK: 'capslock',
    KEY_ENTER: 'enter',
    KEY_SHIFT_R: 'shiftright',
    KEY_CTRL_R: 'ctrlright',
    KEY_BACKSPACE: 'backspace',
    KEY_ALT_R: 'altright',
    KEY_ALT: 'alt',
}

COMMAND = 0
ARG1 = 1
ARG2 = 2
ARG3 = 3


def start_command(command):
    pyautogui.PAUSE = 0
    pyautogui.FAILSAFE = False
    cmd = ''
    arg1 = ''
    arg2 = ''

    command = command.split()

    try:
        index = 0
        for arg in command:
            if index == 0:
                cmd = str(arg)
            elif index == 1:
                if cmd in MOUSE_EVENTS:
                    arg1 = int(arg)
                else:
                    arg1 = str(arg)
            elif index == 2:
                if cmd in MOUSE_EVENTS:
                    arg2 = int(arg)
                else:
                    arg2 = str(arg)
            index += 1
        print(f'Command: {cmd}, argument1: {arg1}, argument2: {arg2}')

        if cmd == EVENT_MOUSEMOVE:
            pyautogui.moveTo(arg1, arg2)

        elif cmd == EVENT_LBUTTONDBLCLK:
            pyautogui.doubleClick(arg1, arg2)

        elif cmd == EVENT_LBUTTONDOWN:
            pyautogui.leftClick(arg1, arg2)

        elif cmd == EVENT_RBUTTONDOWN:
            pyautogui.rightClick(arg1, arg2)

        elif cmd == EVENT_KB_KEY:
            if arg1 in KB_ACTIONS:
                val = KB_ACTIONS.get(arg1)
                print(f'kb_special: {val}')
                pyautogui.press(val)
            else:
                pyautogui.press(arg1)

        else:
            print(f'Other command {cmd}')

    except (IndexError, ValueError) as error:
        print(f'Unknown command: {command} - {error}')

    print('\r\n')
    return
