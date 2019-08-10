""" A program to see which machines a drawing is on, if any. Let the user know, and give them the option to open the
    .mpr file if they choose.

    Inputs:
        drawingNumber -- This is the drawing number excluding any revision information.

    Outputs:
        A printed list of which machines the drawing is on, if none then it will offer to create file using Gen_rec.py.
        The option to open the .mpr file on one of those machines from the terminal will be there, if it exists.
"""
import os
import time
import machineFilePaths
import pyperclip

# list of machine pathways, setting 'if it exists' to false by default, and machine names
vantechPath, vantech, van = machineFilePaths.vantech_parts(), False, 'Vantech'
jasperWeekePath, jasperWeeke, jas = machineFilePaths.jasper_parts(), False, 'JasperWeeke'
fvWeekePath, fvWeeke, fv = machineFilePaths.fordsvile_parts(), False, 'FVWeeke'
bazPath, baz, BAZ = machineFilePaths.baz_parts(), False, 'BAZ'
abdPath, abd, ABD = machineFilePaths.abd_parts(), False, 'Homaghbore'

allPaths = [vantechPath, jasperWeekePath, fvWeekePath, bazPath, abdPath]
foundOnMachine = [vantech, jasperWeeke, fvWeeke, baz, abd]
machineNames = [van, jas, fv, BAZ, ABD]
fileList = {}

# input for drawing look up
# first option is to use the clipboard. Try/Except to validate input is an integer, and then confirm length of input.
# if clipboard isn't validated or user doesn't confirm look up by entering text, then ask for the drawing number to
# look up.
try:
    if int(pyperclip.paste()) >= 6 & int(pyperclip.paste()) <= 8:
        use_clipboard = input('Type anything to look up ' + str(pyperclip.paste()) + '. ')
        if use_clipboard:
            drawingNumber = pyperclip.paste()
        else:
            drawingNumber = input(str('Please enter the drawing number you want to find.\n'))
    else:
        drawingNumber = input(str('Please enter the drawing number you want to find.\n'))
except ValueError:
    drawingNumber = input(str('Please enter the drawing number you want to find.\n'))

# Begin looking for drawing number in machine files
while drawingNumber:
    fileListKey = 1
    for path in allPaths:
        for rootDir, subDir, filenames in os.walk(path):
            for filename in filenames:
                if filename.endswith('.mpr') and filename.startswith(drawingNumber):
                    for i in range(len(machineNames)):
                        if machineNames[i] in path:
                            fullpath = os.path.join(rootDir, filename)
                            foundOnMachine[i] = True
                            print(str(fileListKey) + ': ' + filename + ' found on the ' + machineNames[i]
                                  + ' : ' + time.ctime(os.path.getctime(fullpath)))
                            fileList.update({fileListKey: os.path.join(rootDir, filename)})
                            fileListKey += 1

    # If drawing doesn't exist, offer to make it.
    while not any(foundOnMachine):
        create_file = input('Would you like to create ' + drawingNumber + '?\nOr hit enter to escape.\n')
        if create_file:
            os.startfile("C:\\Users\\scasey\\gen_rec2.bat")
        break

    # Ask which machines, if any, the user wants to open the file up from and prompt for next file to look up
    while any(foundOnMachine):
        print('Type the line number to open the file or just hit enter to look up another file.')
        fileToOpen = input(str(''))
        if not fileToOpen:
            break
        elif int(fileToOpen) in fileList.keys():
            os.startfile(fileList.get(int(fileToOpen)))
            print('Opening ' + drawingNumber + ' from line ' + fileToOpen)
    drawingNumber = input(str('Please enter the drawing number you want to find.\nOr hit enter to escape.\n'))
