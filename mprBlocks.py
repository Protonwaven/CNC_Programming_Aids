import sys


def datahead(x, y, z):
    """This function will set the datahead for the MPR file, including
    overall size, offsets, etc

    Inputs:
        X,Y, and Z -- These are teh overall length, wicth and thickness of the part.

    Output:
        A complete data header
    """
    return ("""[H
VERSION="4.0 Alpha"
WW="6.0.46"
OP="1"
WRK2="1"
SCHN="0"
HSP="0"
O2="0"
O4="0"
O3="0"
O5="0"
SR="0"
FM="1"
ML="2000"
UF="STANDARD"
DN="STANDARD"
GP="0"
GY="0"
GXY="0"
NP="1"
NE="0"
NA="0"
BFS="1"
US="0"
CB="0"
UP="0"
DW="0"
MAT="HOMAG"
INCH="0"
VIEW="NOMIRROR"
ANZ="1"
BES="0"
ENT="0"
_BSX=""" + x + """\n"""
            + '''_BSY=''' + y + '''\n'''
            + '''_BSZ=''' + z + '''\n'''
            + '''_FNX=0.000000
_FNY=0.000000
_RNX=0.000000
_RNY=0.000000
_RNZ=0.000000
_RX=''' + x + '''\n'''
            + '''_RY=''' + y + '''\n'''
            + '''\n'''
            + '''[001
L="''' + x
            + '''"\nKM="LENGTH"
W="''' + y
            + '''"\nKM="WIDTH"
T="''' + z +
            '''"\nKM="THICKNESS"\n
]''')


def coordsysgenrec():
    """This is the coordinate system for a basic rectangle. Starting in the center
    of the long side and moving around the part clockwise

    Inputs:
        None

    Outputs:
        A complete parametric rectangle.
    """

    return ('''1
$E0
KP NEST
X=L/2
Y=0.0
Z=0.0
KO=00
.X=0.000000
.Y=0.000000
.Z=0.000000
.KO=00

$E1
KL 
X=0.0
Y=0.0
.X=0.000000
.Y=0.000000
.Z=0.000000
.WI=0.000000
.WZ=0.000000

$E2
KL 
X=0.0
Y=W
.X=0.000000
.Y=0.000000
.Z=0.000000
.WI=0.000000
.WZ=0.000000

$E3
KL 
X=L
Y=W
.X=0.000000
.Y=0.000000
.Z=0.000000
.WI=0.000000
.WZ=0.000000

$E4
KL 
X=L
Y=0
.X=0.000000
.Y=0.000000
.Z=0.000000
.WI=0.000000
.WZ=0.000000

$E5
KL 
X=L/2
Y=0
.X=0.000000
.Y=0.000000
.Z=0.000000
.WI=0.000000
.WZ=0.000000
''')


def workpiece():
    """This contains the part size, oversize and offset.
    Inputs:
        None

    Outputs:
        The part size oversize, offset, and part offset.
    """

    return ('''
<100 \\WerkStck
LA="L"
BR="W"
DI="T"
FNX="0"
FNY="0"
AX="0"
AY="0"
''')


def comment(program_name, programmer, machine):
    """ Creates a comment with the program number, programmer name, and date of file creation

     Inputs:
        program_name -- this is the generally the drawing number.
        programmer -- name of programmer running it. Please update it if it isn't you
        machine -- if machine is the  Fordsville Weeke it will modify the comment to prevent
        error with WoodWop 4 comment block.

     Output:
        Comment Block for WoodWop 4 or WoodWop 5+
     """
    import datetime
    today = datetime.date.today()
    if 'ford' in machine:
        return '''
<101 \\Kommentar\\
KM="''' + program_name + '''"
KM=""
KM="''' + programmer + '''"
KM="''' + today.strftime('%b/%d/%y') + '''"'''
    else:
        return '''
<101 \\Kommentar\\
KM="''' + program_name + '''"
KM=""
KM="''' + programmer + '''"
KM="''' + today.strftime('%b/%d/%y') + '''"
KAT="Kommentar"
MNM="Comment"
ORI="1"'''


def groupblock(drill_type, *machine):
    """This creates a grouping for drilling. The fuction will call either vertical or horizontal
    drilling functions base on the input drill_type. You will select a local coordinate system, and
    then enter the drill diameter and depth.

    Inputs:
        drill_type -- Will be either vertical or horizontal.

    Outputs:
        A complete drill grouping containing same diameter and depth drills. """

    diameter = ''
    depth = ''
    group_name = ''
    count_in_group = 0
    output = ''
    thru = False

    if drill_type is 'vert':
        diameter = input('Please enter hole diameter in mm for the group.\n')
        depth = input('Please enter hole depth in mm or " thru " for the group.\n')
        group_name = diameter + 'mm bore - ' + depth + 'mm depth'
    if drill_type is 'hor':
        diameter = input('Please enter hole diameter in mm for the group.\n')
        depth = input('Please enter hole depth in mm for the group.\n')
        group_name = diameter + 'mm bore - ' + depth + 'mm depth'
    elif drill_type is 'fast':
        group_name = 'Fastenlink'
    local_coord_sys = input('Select a local coordinate system for the grouping\n'
                            '    1________0\n'
                            '    |        |\n'
                            '    |        |\n'
                            '    |________|\n'
                            '    2        3\n')

    if 'thru' in depth:
        group_name = diameter + 'mm bore - thru'
        thru = True
    loop = True
    drilling = ''
    while loop:
        if 'vert' in drill_type:
            drilling = vertdrill(diameter, depth, thru, machine)
        elif 'hor' in drill_type:
            drilling = hordrill(diameter, depth, local_coord_sys)
        elif 'fas' in drill_type:
            drilling = fastenlink(local_coord_sys)
        output += drilling
        count_in_group += 1
        loop = input('Type anything to keep looping.\n')
    return ('''
<121 \\Block
XP="0.0"
YP="0.0"
ZP="0.0"
AX="1"
AY="1"
RX="0.0"
RY="0.0"
CS="0"
OC="0"
KAT="BlockMakro"
MNM="''' + group_name + '''"
ORI="2"
NM=""
DP="''' + str(count_in_group) + '''"
KO="''' + str(local_coord_sys) + '''"
''' + output)


def vertdrill(diameter, depth, thru, machine):
    """Adds vertical drilling to the grouping.
        Inputs:
            diameter -- diameter of vertical drilling. This is pulled from the group the drill resides in.
            depth -- depth of vertical drill from face. This is pulled from the group the drill resides in.
            thru -- if the drill is thru the part adjustments are made.
            machine -- used for jasper weeke tool number adjustment

        Outputs:
            A single vertical drill process to the group that called this function.
    """
    # Matrix Drilling Standards
    number_of_drills = '1'
    drilling_dis = '32'
    drilling_rotation = '0'

    print('Enter "+" after X to turn on Matrix drilling.\n')
    x = str(input('X: '))
    y = str(input('Y: '))

    # prompts for matrix drilling inputs if selected.
    if x.endswith('+'):
        number_of_drills = input('Please enter the number of drills.\n')
        drilling_dis = input('Please enter the distance between each hole.\n')
        drilling_rotation = input('Please enter the angle of rotation.\n')
        x = x.replace('+', '')
        y = y.replace('+', '')

    # This will end the drilling with out generating a drill process.
    if x and y is False:
        return "\n"

    elif thru:
        if 'jasper' in machine and thru:
            if diameter == '5':
                diameter = '7'
            elif diameter == '10':
                diameter = '9'
        return '''
<102 \\BohrVert
XA="''' + x + '''"
YA="''' + y + '''"
BM="LSL"
DU="''' + str(diameter) + '''"
AN="''' + number_of_drills + '''"
MI="0"
S_="1"
AB="''' + drilling_dis + '''"
WI="''' + drilling_rotation + '''"
ZT="0"
RM="0"
VW="0"
HP="0"
SP="0"
YVE="0"
WW="60,61,62,86,87,88,90,91,92,148,149,150,191,192"
ASG="2"
KAT="Bohren vertikal"
MNM="Vertical drilling"
ORI="2"
MX="0"
MY="0"
MZ="0"
MXF="1"
MYF="1"
MZF="1"
SYA="0"
SYV="0"
KO="00"'''

    elif not thru:
        return '''
<102 \\BohrVert
XA="''' + x + '''"
YA="''' + y + '''"
BM="LS"
TI="''' + str(depth) + '''"
DU="''' + str(diameter) + '''"
AN="''' + number_of_drills + '''"
MI="0"
S_="1"
AB="''' + drilling_dis + '''"
WI="''' + drilling_rotation + '''"
ZT="0"
RM="0"
VW="0"
HP="0"
SP="0"
YVE="0"
WW="60,61,62,86,87,88,90,91,92,148,149,150,191,192"
ASG="2"
KAT="Bohren vertikal"
MNM="Vertical drilling"
ORI="2"
MX="0"
MY="0"
MZ="0"
MXF="1"
MYF="1"
MZF="1"
SYA="0"
SYV="0"
KO="02"'''


def hordrill(diameter, depth, local_coord_sys):
    """Adds horizontal drilling to the grouping.
    Inputs:
        diameter -- diameter of horizontal drilling. This is pulled from the group the drill resides in.
        depth -- depth of horizontal drill from face. This is pulled from the group the drill resides in.

    Outputs:
        A single horizontal drill process to the group that called this function. """

    x = str(input('X: '))
    y = str(input('Y: '))
    z = str(input('Z: '))
    drill_mode = ''

    # Compensation for "mirrored" zones selection.
    if local_coord_sys is '0':
        drill_mode = input('Select direction to drill from:\n'
                           '     ___yp___ 0\n'
                           '    |        |\n'
                           '  xm|        |xp\n'
                           '    |________|\n'
                           '        ym    \n')
    if local_coord_sys is '1':
        drill_mode = input('Select direction to drill from:\n'
                           '  1  ___yp___ \n'
                           '    |        |\n'
                           '  xp|        |xm\n'
                           '    |________|\n'
                           '        ym    \n')
    if local_coord_sys is '2':
        drill_mode = input('Select direction to drill from:\n'
                           '     ___ym___ \n'
                           '    |        |\n'
                           '  xp|        |xm\n'
                           '    |________|\n'
                           '   2    yp    \n')
    if local_coord_sys is '3':
        drill_mode = input('Select direction to drill from:\n'
                           '     ___ym___ \n'
                           '    |        |\n'
                           '  xm|        |xp\n'
                           '    |________|\n'
                           '        yp    3\n')

    if not z:
        print('Horizontal Drill error 2:\n  Error with Z value.\n')
        sys.exit()
    return '''
<103 \\BohrHoriz\\
MI="0"
XA="''' + x + '''"
YA="''' + y + '''"
ZA="''' + z + '''"
DU="''' + diameter + '''"
TI="''' + depth + '''"
ANA="20"
BM="''' + drill_mode + '''"
LA="0"
AB="32"
BM2="STD"
ZT="0"
RM="0"
VW="0"
HP="0"
SP="0"
YVE="0"
WW="50,51,52,53,54,56,60,61,62,93,94,95,153,151,154,155,158,159"
ASG="2"
KAT="Horizontalbohren"
MNM="Horizontal drilling"
ORI="1"
MX="0"
MY="0"
MZ="0"
MXF="1"
MYF="1"
MZF="1"
SYA="0"
SYV="0"
KO="00"'''


def pocket():
    """ Adds a pocket process to the file. The pocket will not be in group

    Inputs:
        Machine -- This will determine which tool number is used.

    Outputs:
        One pocket process.
    """
    x_center = input('Please enter X center.\n')
    y_center = input('Please enter Y center.\n')
    pocket_length = input('Please enter the overall length of the pocket.\n')
    pocket_width = input('Please enter the overall width of the pocket.\n ')
    corner_radius = input('Please enter the corner radius of the pocket.\n')
    depth = input('Please enter the depth of the pocket.\n')
    tool = ''
    try:
        if float(depth) < 6:
            tool = '130'
        else:
            tool = '128'
    except ValueError:
        import re
        if float(re.sub(r'\D', '', depth)) < 6:
            tool = '130'
        else:
            tool = '128'

    return'''
<112 \\Tasche\\
XA="''' + x_center + '''"
YA="''' + y_center + '''"
LA="''' + pocket_length + '''"
BR="''' + pocket_width + '''"
RD="''' + corner_radius + '''"
WI="0"
TI="''' + depth + '''"
ZT="0"
XY="80"
T_="''' + tool + '''"
F_="5"
DS="1"
OSZI="0"
BL="0"
OSZVS="0"
SM="0"
S_="STANDARD"
ZU="0"
HP="0"
SP="0"
YVE="0"
WW="1,2,3,401,402,403"
ASG="2"
KG="0"
RP="STANDARD"
KAT="Tasche"
MNM="Trimming Pocket Vertical"
ORI="1"
MX="0"
MY="0"
MZ="0"
MXF="1"
MYF="1"
MZF="1"
SYA="0"
SYV="0"
KO="00"'''


def fastenlink(local_coord_sys):
    x = str(input('X: '))
    y = str(input('Y: '))
    direction = input('Please enter the direction for the fastenlink.\n'
                      '         8\n'
                      '         |\n'
                      '     4--- ---6\n'
                      '         |\n'
                      '         2\n')
    hole_up = '0'
    hole_right = '0'
    hole_down = '0'
    hole_left = '0'
    if direction == '8':
        hole_up = '1'
    elif direction == '6':
        hole_right = '1'
    elif direction == '2':
        hole_down = '1'
    elif direction == '4':
        hole_left = '1'
    else:
        print('Fastenlink Error 1:\n    Fastenlink direction invalid')
        sys.exit()

    # Compensation for "mirrored" zones selection.
    if local_coord_sys is '1':
        temp = hole_left
        hole_left = hole_right
        hole_right = temp
    if local_coord_sys is '2':
        temp = hole_left
        hole_left = hole_right
        hole_right = temp
        temp = hole_up
        hole_up = hole_down
        hole_down = temp
    if local_coord_sys is '3':
        temp = hole_up
        hole_up = hole_down
        hole_down = temp

    if x and y is False:
        return "\n"
    return '''\n
<139 \\Komponente\\
IN="Fastenlink.mpr"
XA="''' + x + '''"
YA="''' + y + '''"
ZA="0.0"
EM="0"
VA="North ''' + hole_up + '''"
VA="East ''' + hole_right + '''"
VA="South ''' + hole_down + '''"
VA="West ''' + hole_left + '''"
VA="Angle 0"
VA="L 30"
VA="W 50"
VA="z 18.3"
VA="XXXXXXX 99999"
VA="D1 .211*25.4"
VA="L1 -.150*25.4"
VA="L2 .150*25.4"
VA="W1 L1"
VA="nAngle IF South = 0 AND East = 0 AND West = 0 AND North = 1 AND Angle = 0 THEN 0 ELSE 0"
VA="sAngle IF South = 1 AND East = 0 AND West = 0 AND North = 0 AND Angle = 0 THEN 180 ELSE 0"
VA="eAngle IF South = 0 AND East = 1 AND West = 0 AND North = 0 AND Angle = 0 THEN 270 ELSE 0"
VA="wAngle IF South = 0 AND East = 0 AND West = 1 AND North = 0  AND Angle = 0 THEN 90 ELSE 0"
VA="a1 IF Angle<>0 AND West = 0 AND South = 0 AND East = 0 AND North = 0 THEN 1 ELSE 0"
VA="a2 IF Angle = 0 AND West = 1 AND South = 0 AND East = 0 AND North = 0 THEN 1 ELSE 0"
VA="a3 IF Angle = 0 AND West = 0 AND South = 1 AND East = 0 AND North = 0 THEN 1 ELSE 0"
VA="a4 IF Angle = 0 AND West = 0 AND South = 0 AND East = 1 AND North = 0 THEN 1 ELSE 0"
VA="a5 IF Angle = 0 AND West = 0 AND South = 0 AND East = 0 AND North = 1 THEN 1 ELSE 0"
KAT="Komponentenmakro"
MNM="Fastenlink"
ORI="1"
KO="00"'''


def abd(edge):
    """
    This will generate 1 abd_multi_eng component. Each component can only have a singe diameter and depth.

    Input:
        edge -- this will selcet the edge that you will be drilling into

    Output:
        A complete abd_multi_eng component
    """

    diameter = str(input('Please enter the diameter of the hole.\n'))
    depth = str(input('Please enter the depth of the hole.\n'))
    zpos = str(input('Please enter the Z value of the hole.\n'))
    glue = '0'
    dowel = '0'
    if diameter == '8' and depth == '24':
        insert = input('Type yes for gluing and dowels.\n')
        if insert == 'yes':
            glue = '1'
            dowel = '1'
    pos = ['0', '0', '0', '0', '0', '0', '0', '0']
    for i in range(8):
        pos[i] = str(input('Please enter the position of the hole\n'))
        if pos[i] == '':
            pos[i] = '0'
            break
    return """\n
<139 \\Komponente\\
IN="abd_multi_enu.mpr"
XA="0.0"
YA="0.0"
ZA="0.0"
EM="0"
VA="Edge """ + edge + """"
VA="Pos """ + pos[0] + """"
VA="Pos2 """ + pos[1] + """"
VA="Pos3 """ + pos[2] + """"
VA="Pos4 """ + pos[3] + """"
VA="Pos5 """ + pos[4] + """"
VA="Pos6 """ + pos[5] + """"
VA="Pos7 """ + pos[6] + """"
VA="Pos8 """ + pos[7] + """"
VA="ZPos """ + zpos + """"
VA="Diameter """ + diameter + """"
VA="depth """ + depth + """"
VA="dowel """ + dowel + """"
VA="glue """ + glue + """"
VA="number 1"
VA="grid 32"
VA="center 1"
VA="inch 0"
KAT="Komponentenmakro"
MNM="abd_multi_enu"
ORI="4"
KO="00"""


def routing():
    """Nesting route to the part.
    Inputs:
        None

    Outputs:
        A routing process with the nesting option check. Starts and stops on contour 1 point 1."""

    return ('''
<105 \\Konturfraesen
EA="1:0"
MDA="SEN"
STUFEN="0"
BL="0"
WZS="1"
OSZI="0"
OSZVS="0"
ZSTART="0"
ANZZST="0"
RK="WRKL"
EE="1:0"
MDE="SEN_AB"
EM="1"
RI="1"
TNO="128"
SM="0"
S_="STANDARD"
F_="10"
AB="0"
AF="3"
AW="0"
BW="0"
VLS="0"
VLE="0"
ZA="-.2"
SC="0"
HP="0"
SP="0"
YVE="0"
WW="1,2,3,401,402,403"
ASG="2"
KG="0"
RP="STANDARD"
RSEL="0"
RWID="0"
KAT="Frisen"
MNM="Vertical trimming"
ORI="1"
MX="0"
MY="0"
MZ="0"
MXF="1"
MYF="1"
MZF="1"
SYA="0"
SYV="0"''')


def graindir():
    """This adds the graindir.mpr component to the file.
    Inputs:
        None

    Outputs:
        Component containing graindir.mpr."""
    return ('''

<139 \\Komponente
IN="grainDir.mpr"
XA="0.0"
YA="0.0"
ZA="0.0"
EM="0"
VA="L L"
VA="W W"
VA="T T"
KAT="Component macro"
MNM="grainDir"
ORI="2"
KO="00"''')
