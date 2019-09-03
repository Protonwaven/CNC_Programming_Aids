"""A program to search all .mpr file within a specific directory for a certain string, commonly a component name, and
count how many times it appears. Then print the results to a new file and open file for review.

Inputs:
    scanFolder -- this is the folder you wish to scan. It must be entered as an absolute path.
        example: c:\\python\\quotes
    findString -- This is the string you wish to find.
        example: Tis but a scratch

Outputs:
    output -- A file with the results of the scanning and counting.
"""
import os
import re

# Get the path to scan.Then run a quick regex check to see if the input matches the basic windows path
# format. If the matching fails, reprompt for correct input
scanFolder = input('Select absolute path to the folder to scan:\n')
validatePathRegex = re.compile(r'[a-z,A-Z]:\\?(\\?\w*\\?)*')
mo = validatePathRegex.search(scanFolder)
while not mo:
    print('Path is not valid. Please re-enter path.')
    scanFolder = input('Please renter the absolute path to the folder to scan:\n')
    mo = validatePathRegex.search(scanFolder)

# Enter the string you wish to find.
findString = input('Enter the text to find:\n' )

os.chdir(scanFolder)
count = 0
outputList = []
with open('found_%s_or_not.txt' % findString, 'w') as output:
    for root, subdir, files in os.walk(scanFolder):
        for file in files:
            if os.path.join(file).endswith('.mpr'):
                fullpath = os.path.join(root, file)
                with open(fullpath, 'r') as f:
                    for lines in file:
                        line = f.read()
                        if findString in line:
                            outputList.append(os.path.join(root, file) + ' contains ' + findString + '\n')
                            count += 1
    outputList = ['The total count is ' + str(count) + '\n\n'] + outputList
    output.write(''.join(outputList))
    os.startfile(output)
