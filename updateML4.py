"""A program to update the ML4 files from the ML4 folder on common and sending it to all machines.

"""

import os
import shutil
import time

# Common ML4
ML4 = 'Z:\\Common\\ML4'

# Vantech ML4
Vantech_ML4 = 'Z:\\Common\\Vantech\\ml4'

# Jasper Weeke ML4
Jasper_ML4 = 'Z:\\15th St\\JasperWeeke\\ml4'

# Fordsville Weeke ML4
Fordsville_ML4 = 'Z:\\15th St\\FVWeeke\\ml4'

# BAZ ML4
BAZ_ML4 = 'Z:\\15th St\\Homag_BAZ\\BAZ\\ml4'

Machines = [Vantech_ML4, Jasper_ML4, Fordsville_ML4, BAZ_ML4]

for folderName, subfolders, filenames in os.walk(ML4):
    for filename in filenames:
        if filename.endswith('.mpr'):
            fullpath = os.path.join(folderName, filename)
            for path in Machines:
                shutil.copy(fullpath, path)
                print('Copying from {} to {}'.format(fullpath, path))
                # TODO add email to notify other programmers of Component change

time.sleep(6)
