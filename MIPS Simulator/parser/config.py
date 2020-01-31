import sys

file_config = open(sys.argv[4],'r')

adder = 0
multiplier = 0
divider = 0
memory = 0
iCache = 0
dCache = 0
isAdderPipelined = True
isMultiplierPipelined = True
isDividerPipelined = False

for line in file_config:
    res = ''
    digit = 0
    for i in line:
        if i.isdigit():
            res = res + i
    digit = int(res)
    if(line.__contains__('adder')):
        adder = digit
        if(line.__contains__('no')):
            isAdderPipelined = False
    if (line.__contains__('Multiplier')):
        multiplier = digit
        if (line.__contains__('no')):
            isMultiplierPipelined = False
    if (line.__contains__('divider')):
        divider = digit
        if (line.__contains__('yes')):
            isAdderPipelined = True
    if (line.__contains__('memory')):
        memory = digit
    if (line.__contains__('I-Cache')):
        iCache = digit
    if (line.__contains__('D-Cache')):
        dCache = digit







file_config.close()