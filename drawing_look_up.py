"""A program to see which machines a drawing is on, if any. Let the user know, and give them the option to open the
.mpr file if they choose.

Inputs:
    drawingNumber -- This is the drawing number excluding any revision information.
    import from windows clipboard -- This option is automatic. It the clipboard is between 6 - 8 numbers long it
    will prompt with the option to press 1 and look up that drawing.

Outputs:
    A printed list of which machines the drawing is on (along with date/time of last file modification), if none
    then it will offer to create file using Gen_rec.py. If Gen_rec.py is not available, the user will be notified
    and the program will move on. The option to open the .mpr file on one of those machines from the terminal will
    be there, if it exists.
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
bimaPath, bima, BIMA = machineFilePaths.bima_parts(), False, 'Bima'
morbPath, morb, MORB = machineFilePaths.morb_parts(), False, 'Morb'

allPaths = [vantechPath, jasperWeekePath, fvWeekePath, bazPath, abdPath, bimaPath, morbPath]
foundOnMachine = [vantech, jasperWeeke, fvWeeke, baz, abd, bima, morb]
machineNames = [van, jas, fv, BAZ, ABD, BIMA, MORB]
fileList = {}

# input for drawing look up
try:
    if int(pyperclip.paste()) >= 6 & int(pyperclip.paste()) <= 8:
        use_clipboard = input('Type 1 to look up ' + str(pyperclip.paste()) + '\nElse, type in the drawing number you '
                                                                              'want to find.\n')
        if use_clipboard == '1':
            drawingNumber = pyperclip.paste().strip()
        else:
            drawingNumber = use_clipboard
    else:
        drawingNumber = input(str('Please enter the drawing number you want to find.\n'))
except ValueError:
    drawingNumber = input(str('Please enter the drawing number you want to find.\n'))

# Begin looking for drawing number in machine files
while drawingNumber:
    drawingNumber.strip()
    fileListKey = 1
    for path in allPaths:
        for rootDir, subDir, filenames in os.walk(path):
            for filename in filenames:
                if (filename.endswith('.mpr') or filename.endswith('.ard')) and filename.startswith(drawingNumber):
                    for i in range(len(machineNames)):
                        if machineNames[i] in path:
                            fullpath = os.path.join(rootDir, filename)
                            foundOnMachine[i] = True
                            print(str(fileListKey) + ': ' + filename + ' found on the ' + machineNames[i]
                                  + ' : ' + time.ctime(os.path.getctime(fullpath)))
                            fileList.update({fileListKey: os.path.join(rootDir, filename)})
                            fileListKey += 1

    # If drawing doesn't exist, offer to make it.
    if not any(foundOnMachine):
        create_file = input('Would you like to create ' + drawingNumber + '?\nOr hit enter to escape.\n')
        try:
            if create_file:
                with open('handOff.txt', 'w') as handOff:
                    handOff.write(drawingNumber)
                os.startfile("C:\\Users\\scasey\\gen_rec2.bat")
            break
        except FileNotFoundError:
            print('Nice try but you don\'t have access to this function.')
            break

    # Ask which machines, if any, the user wants to open the file up from and prompt for next file to look up
    isFileOpen = False
    while any(foundOnMachine):
        fileToOpen = input(str('Type the line number to open the file or just hit enter to look up a different file.'))
        if not fileToOpen:
            break
        elif int(fileToOpen) in fileList.keys():
            os.startfile(fileList.get(int(fileToOpen)))
            print('Opening ' + drawingNumber + ' from line ' + fileToOpen)
    drawingNumber = input(str('Please enter the drawing number you want to find.\nOr hit enter to end the program.\n'))
