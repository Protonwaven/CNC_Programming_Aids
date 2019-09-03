""" A quick script to pull up a drawing in Solid Edge using GUI automation. SE should be already open and logged into
or else the commands will not work.

Inputs:
    drawingNumber -- This is the drawing number excluding any revision information.
    import from windows clipboard -- This option is automatic. It the clipboard is between 6 - 8 numbers long it
    will prompt with the option to press 1 and look up that drawing.

Outputs:
    Opening SolidEdge to the input drawing.
"""
import pyautogui
import pyperclip

# Offer to use the clipboard, or manually type in drawing number to open in SE
try:
    if int(pyperclip.paste()) >= 6 & int(pyperclip.paste()) <= 8:
        use_clipboard = input('Type "1" to look up ' + str(pyperclip.paste()) + '\nIf not, just type in the drawing '
                                                                                'number.\n')
        if use_clipboard == '1':
            drawingNumber = pyperclip.paste()
        else:
            drawingNumber = use_clipboard
    else:
        drawingNumber = input(str('Please enter the drawing number you want to find.\n'))
except ValueError:
    drawingNumber = input('Please enter the drawing you want to pull up.\n')

# Try to open Solid Edge and enter drawing number into search bar.
pyautogui.PAUSE = 2
# click on the SE icon on the taskbar
pyautogui.click(422, 1057)
pyautogui.PAUSE = 1.5
# click on the app bar in SE
pyautogui.click(1943, 20)
pyautogui.PAUSE = 1.5
# click on the open file button in SE
pyautogui.click(2148, 168)
pyautogui.PAUSE = 1.5
# click on the item id in the open file menu
pyautogui.click(2870, 362)
pyautogui.PAUSE = 1.5
pyautogui.hotkey('ctrl', 'a')
pyautogui.typewrite(['delete'])
pyautogui.typewrite(drawingNumber)
pyautogui.typewrite(['enter'])
pyautogui.PAUSE = 1.5
pyautogui.typewrite(['enter'])
