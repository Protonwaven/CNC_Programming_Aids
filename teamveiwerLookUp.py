"""A quick script to pull up TeamCenter and search for the drawing using GUI
automation.

    Input -- Will load drawing number from Windows clipboard, or terminal.
"""

import pyautogui
import pyperclip

try:
    if int(pyperclip.paste()) >= 6 & int(pyperclip.paste()) <= 8:
        use_clipboard = input(f'Type 1 to look up {str(pyperclip.paste())}'
                              f'\nElse, type in the drawing number you want '
                              f'to find.\n')
        if use_clipboard == '1':
            drawingNumber = pyperclip.paste().strip()
        else:
            drawingNumber = use_clipboard
    else:
        drawingNumber = input(str('Please enter the drawing number you want to find.\n'))
except ValueError:
    drawingNumber = input(str('Please enter the drawing number you want to find.\n'))

iePosition = (91, 1059)

pyperclip.copy(drawingNumber)
pyautogui.click(iePosition)
pyautogui.sleep(3)
pyautogui.hotkey('ctrl', 'v')
pyautogui.hotkey('enter')
