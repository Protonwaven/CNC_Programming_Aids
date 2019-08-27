# CNC Programmer Aids 
A collection of programs to assist in writing and managing of CNC programs.

Note: machineFilePath.py is just each needed file path bundled together for convenience and easy of management. 

drawing_look_up.py -- Scans through all machine folders to find which machine the program is on, and the date of its last modification. 

findAndReplace.py and scanAndCountString.py -- Read through all MPR files in specified folder to find and replace, or count, the enter string. 

Gen_Rec.py and mprBlocks.py -- These allow for the creation of generic square mpr programs through the terminal with options for vertical, horizontal drilling, pockets, and Fastenlink componets. Based off the desired machine to0 save too, the availbe options change. Please note that the only shape currently available is a rectangle.

Pull_up_drawing_SE.py -- A simple GUI automation to pull the entered program, or a program in teh Windows clipboard, in SolidEdge.

updateML4.py -- Quickly update any changes to the common ML4 files to all machines.   