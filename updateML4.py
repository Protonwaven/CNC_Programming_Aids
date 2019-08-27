"""
    A program to update the ML4 files from the ML4 folder on common and sending it to all machines.

    Input:
        None.

    Output:
        A print out in the terminal of all files that have been updated.

"""

import os
import shutil
import time
import machineFilePaths

# define ML4 folder locations and put them in a list to iterate over.
ML4 = machineFilePaths.common_ml4()
Vantech_ML4 = machineFilePaths.vantech_ml4()
Jasper_ML4 = machineFilePaths.jasper_ml4()
Fordsville_ML4 = machineFilePaths.fordsvile_ml4()
BAZ_ML4 = machineFilePaths.baz_ml4()

Machines = [Vantech_ML4, Jasper_ML4, Fordsville_ML4, BAZ_ML4]

for folderName, subfolders, filenames in os.walk(ML4):
    for filename in filenames:
        if filename.endswith('.mpr'):
            fullpath = os.path.join(folderName, filename)
            for path in Machines:
                shutil.copy(fullpath, path)
                print('Copying from {} to {}'.format(fullpath, path))
print('\nAll files have been updated.\n\nNow please send an email to all other programmers to remind them to update '
      'their folders has well.\n')

# Added sleep(12) to allow the user to read the terminal.
time.sleep(12)
