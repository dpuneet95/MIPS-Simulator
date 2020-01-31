import sys

fileData = open(sys.argv[3],'r')

R = []

for value in fileData:
    valueClean = value.strip(' ')
    integerData = int(valueClean,2)
    R.append(integerData)

fileData.close()

