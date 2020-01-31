import sys

fileData = open(sys.argv[2],'r')

decimalList = []
binaryList =  []

for dataLine in fileData:
    dataClean = dataLine.strip(' ')
    binaryList.append(dataClean)
    decimalData = int(dataClean,2)
    decimalList.append(decimalData)

fileData.close()

