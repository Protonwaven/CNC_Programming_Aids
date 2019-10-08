"""A Quick clean up script to sort files for the JW. Filters based on file
type and if file starts with digits"""

import os
import shutil

rootdir = os.listdir(r'\\nts141\KOSHopFloor\15th St\JasperWeeke')
files = []
subdirs = []

for file in rootdir:
    if file.endswith('.mpr'):
        files.append(file)
    if os.path.isdir(f'\\\\nts141\\KOSHopFloor\\15th St\\JasperWeeke\\{file}'):
        subdirs.append(file)


for file in files:
    for fold in subdirs:
        if file[0:3] == fold[0:3] and file[0:3].isdigit():
            try:
                shutil.move(os.path.join(f'\\\\nts141\\KOSHopFloor\\15th '
                                     f'St\\JasperWeeke\\{file}'),
                        os.path.join(f'\\\\nts141\\KOSHopFloor\\15th St\\'
                                     f'JasperWeeke\\{fold}'))
            except shutil.Error:
                print(f'File {file} was not printed due to a '
                      f'shutil.Error\nPlease review.')
                continue
