"""Terminal Based program to create a basic rectangle program. Depending on the machine you enter will prompt for
different options. Currently supported machines are the Vantechs, Jasper and Fordsville Weeke, and the ABD. After
generating the generated file will open in WoodWop for review.

Inputs:
    Almost all inputs are numbers, but are treated has string since the generated file is all text.

Outputs:
    A complete ready-to-run MPR file
    # TODO add a clean up to remove groups or other processes with blank data

"""

import mprBlocks
import os
import sys

# Programmer's name is stamped on every generated file.
programmer = 'SCasey'

# Enter machine and based on that selection determine path to save file and options for file generation.
program_name = input('Please enter the name of the program.\n')
machine = input('Enter vantech, jasper, ford or abd.\n')
machine_path = ''
if 'vantech' in machine:
    machine_path = 'Z:\\Common\\Vantech\\Parts\\'
elif 'jasper' in machine:
    machine_path = 'Z:\\15th St\\JasperWeeke\\'
elif 'ford' in machine:
    machine_path = 'Z:\\15th St\\FVWeeke\\mp4\\'
elif 'abd' in machine:
    machine_path = 'Z:\\Common\\Homaghbore\\'
else:
    print('Machine Name Error 1:\n  Invalid machine name entered. ')
    sys.exit()
fullpath = f'{machine_path}{program_name}.mpr'


# These variables equate to L, W, and T in WoodWop
length = input('Please enter the length of the part.\n')
width = input('Please enter the width of the part.\n')
thickness = input('Please enter the thickness of the part.\n')

with open(fullpath, 'w') as f:
    # This is standard across all machines, "removed + mprBlocks.comment(program_name, programmer, machine "
    header = (mprBlocks.datahead(length, width, thickness) + mprBlocks.coordsysgenrec()
              + mprBlocks.workpiece())

    # Only option for abd machine.
    if 'abd' in machine:
        abd_output = ''
        edge_selection = ('Please Select an edge: \n'
                          '\n'
                          '        ___1___\n'
                          '       |        |\n'
                          '      4|        |2\n'
                          '       |________|\n'
                          '           3\n')
        edge = str(input(edge_selection))
        while edge:
            abd_output += mprBlocks.abd(edge)
            edge = str(input(edge_selection))
    # Options for Vantech, Jasper and Fordsville Weeke. Will exclude ABD. Since it cant proform
    # any of these functions.
    # Entering a blank line in group_repeat will cause it to move to the next function.
    elif 'van' or 'jas' or 'for' in machine and 'abd' not in machine:
        group_repeat = input('Do you want to add a vertical drill group?\n')
        drill_type = 'vert'
        vert_drilling_output = ''
        while group_repeat:
            if vert_drilling_output is False:
                break
            drilling = mprBlocks.groupblock(drill_type, machine)
            vert_drilling_output = vert_drilling_output + '\n' + drilling
            group_repeat = input('Would you like to add another vertical drill group?\n')

        # The only the Weekes can proform this function.
        if 'jas' or 'for' in machine:
            group_repeat = input('Do you want to add a horizontal drill group?\n')
            drill_type = 'hor'
            hor_drilling_output = ''
            while group_repeat:
                if hor_drilling_output is False:
                    break
                drilling = mprBlocks.groupblock(drill_type)
                hor_drilling_output = hor_drilling_output + '\n' + drilling
                group_repeat = input('Would you like to add another horizontal drill group?\n')

        group_repeat = input('Do you want to add a Fastenlink group?\n')
        drill_type = 'fast'
        fastenlink_output = ''
        while group_repeat:
            if fastenlink_output is False:
                break
            drilling = mprBlocks.groupblock(drill_type)
            fastenlink_output = fastenlink_output + '\n' + drilling
            group_repeat = input('Would you like to add another Fastenlink group?\n')

        group_repeat = input('Do you want to add a Pocket?\n')
        pocket_output = ''
        while group_repeat:
            if pocket_output is False:
                break
            pocket = mprBlocks.pocket()
            pocket_output = pocket_output + '\n' + pocket
            group_repeat = input('Would you like to add another Pocket?\n')

    footer = ''

    if 'vantech' in machine:
        hor_drilling_output = ''
        footer = (mprBlocks.routing() + mprBlocks.graindir())

    if 'abd' in machine:
        text = (header + abd_output + footer + '!')

    else:
        text = (header + vert_drilling_output + hor_drilling_output + fastenlink_output + pocket_output + footer + '!')
    f.write(str(text))
    os.startfile(fullpath)
