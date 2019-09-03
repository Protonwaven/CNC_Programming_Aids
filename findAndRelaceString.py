"""Enter a pathway to scan, a string to find and string if replace text found.

Inputs:
    scan_folder -- the absolute pathway to the folder you wish to scan reasonable checks are made to ensure format
    it close to correct
    find_string -- the string you wish to find in those files
    replace_string -- the string you are replacing find_string with. There can be a multi-line replace. Due to codecs
    issues, terminal input must be changed to unicode_escape for correct line breaks in .mpr files.

Outputs:
    A revised .mpr file and a .txt with notes regarding the number of files changed, the found
    and the replaced text and the time it took to  complete.
"""
import os
import re
import time
import sys

# Enter path and check input for standard pathway format
scan_folder = input('Enter the absolute path to scan:\n')
validate_path_regex = re.compile(r'[a-z,A-Z]:\\?(\\?\w*\\?)*')
mo = validate_path_regex.search(scan_folder)
if mo is None:
    print('Path is not valid. Please re-enter path.\n')
    time.sleep(10)
    sys.exit()

os.chdir(scan_folder)

# Decide on multi-line edit. An empty string is False for the Boolean expressions below.
multi_line = input('If you would like to edit multiple lines, please enter 9, if not, simply hit enter.\n')

# Get find/replaceStrings, and then confirm that inputs are correct.
find_string = input('Enter the text you wish to find:\n')
replace_string = input('Enter the text to replace:\n')
if multi_line == '9':
    find_string = find_string.encode('utf8').decode('unicode_escape')
    replace_string = replace_string.encode('utf8').decode('unicode_escape')
    print('You will be editing multiple line, please be careful and triple check the confirmation below.'
          + ' Eliminating certain lines could cause the errors on the machinery. \n')

permission = input('Please confirm you want to replace: \n'
                   + find_string
                   + '\nwith\n'
                   + replace_string + ' in ' + scan_folder + ' directory.'
                   + '\n\nType "yes" to continue.\n')
if permission == 'yes':
    start = time.time()
    change_count = 0
    # Context manager for results file.
    with open('find_and_replace_results.txt', 'w') as results:
        for root, subdirs, files in os.walk(scan_folder):
            for file in files:
                # ignore files that don't endwith '.mpr'
                if os.path.join(root, file).endswith('.mpr'):
                    fullpath = os.path.join(root, file)
                    # context manager for each file opened
                    with open(fullpath, 'r+') as f:
                        text = f.read()
                        # only add to changeCount if find_string is in text
                        if find_string in text:
                            change_count += 1
                        # move cursor back to beginning of the file
                        f.seek(0)
                        f.write(text.replace(find_string, replace_string))
        if multi_line:
            results.write(str(change_count) + ' files have been modified to replace\n'
                          + find_string + '\nwith\n' + replace_string + '.\n')
        else:
            results.write(str(change_count) + ' files have been modified to replace '
                          + find_string + ' with ' + replace_string + '.\n')
    print('Done with replacement')
    end = time.time()
    print('Program took ' + str(round((end - start), 4)) + ' secs to complete.\n')
    print(str(change_count) + ' Files replaced')
else:
    print('Find and replace has not been executed')
