# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 09:28:30 2019

@author: scasey
"""

# search each file in a folder for a string, then print the name 
# of each file with that string to another file.

import os, re

scanFolder = input('Select absolute path to folder to scan:\n')                 #get file dir that you want to scan

validatePathRegex = re.compile(r'[a-z,A-Z]:\\?(\\?\w*\\?)*')                       #this checks for a valid path format
mo = validatePathRegex.search(scanFolder)                                          #exp. c:\spam\bacon\
if mo == None:
    print('Path is not valid. Please re-enter path.\n')
    import sys
    sys.exit()

os.chdir(scanFolder)                                                            #chdir to scanFolder 
findString = input('Enter the text to find:\n' )                                #get text string to search for

count = 0
outputList = []
with open('found_%s_or_not.txt' % findString, 'w') as output:                   #open output with context manager
    for root, subdir, files in os.walk(scanFolder):                             #begin walking down file tree 
        for file in files:                                  
                if os.path.join(file).endswith('.mpr'):                             #confirm we're only checking MPR files                
                    fullpath = os.path.join(root, file)                             #create the fullpath to each file                
                    with open(fullpath, 'r') as f:                                  #open file with context manager
                        for lines in file:
                            line = f.read()                                         #read line in file
                            if findString in line:                                  #if findString found in file, write fullpath to output                             
                                outputList.append(os.path.join(root, file) + ' contains ' + findString + '\n') 
                                count += 1
    outputList = ['The total count is ' + str(count) + '\n\n'] + outputList
    output.write(''.join(outputList))
print('Done')