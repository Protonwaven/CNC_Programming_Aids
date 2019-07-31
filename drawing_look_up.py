""" A program to see which machines a drawing is on, if any. Let the user know, and give them the option to open the
    .mpr file if they choose.

    Inputs:
        drawingNumber -- This is the drawing number excluding any revisions.

    Outputs:
        A printed list of which machines the drawing is on, if none then it will offer to create file using Gen_rec.py.
        The option to open the .mpr file on one of those machines from the terminal will be there, if it exists.
"""
import os
import time

# list of machine pathways, if it exists, and machine names
vantechPath, vantech, van = '\\\\nts141\\KOShopFloor\\Common\\Vantech\\Parts', False, 'Vantech'
jasperWeekePath, jasperWeeke, jas = '\\\\nts141\\KOShopFloor\\15th St\\JasperWeeke', False, 'JasperWeeke'
fvWeekePath, fvWeeke, fv = '\\\\nts141\\KOShopFloor\\15th St\\FVWeeke\\mp4', False, 'FVWeeke'
bazPath, baz, BAZ = '\\\\nts141\\KOShopFloor\\15th St\\Homag_BAZ\\BAZ\\mp4', False, 'BAZ'
abdPath, abd, ABD = '\\\\nts141\\KOShopFloor\\Common\\Homaghbore', False, 'Homaghbore'

allPaths = [vantechPath, jasperWeekePath, fvWeekePath, bazPath, abdPath]
foundOnMachine = [vantech, jasperWeeke, fvWeeke, baz, abd]
machineNames = [van, jas, fv, BAZ, ABD]
fileList = {}

drawingNumber = input(str('Please enter the drawing number you want to find.\n'))

while drawingNumber:
    fileListKey = 1
    for path in allPaths:
        for rootDir, subDir, filenames in os.walk(path):
            for filename in filenames:
                if filename.endswith('.mpr') and filename.startswith(drawingNumber):
                    for i in range(len(machineNames)):
                        if machineNames[i] in path:
                            # Get Last Modified Data
                            fullpath = os.path.join(rootDir, filename)

                            # Get file
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

    # Ask which machines, if any, the user wants to open the file up from.
    while any(foundOnMachine):
        print('Type the line number to open the file or just hit enter to look up another file.')
        fileToOpen = input(str(''))
        if not fileToOpen:
            break
        elif int(fileToOpen) in fileList.keys():
            os.startfile(fileList.get(int(fileToOpen)))
            print('Opening ' + drawingNumber + ' from line ' + fileToOpen)
    drawingNumber = input(str('Please enter the drawing number you want to find.\nOr hit enter to escape.\n'))
