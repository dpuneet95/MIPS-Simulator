import register

dCache = [[0 for x in range(8)] for y in range(2)]

var1 = 0
var2 = 0
var3 = 0
var4 = 0
cacheHits = 0

def search(currVal, data_value, displacement, isDouble):
    global cacheHits

    for row in range(0, 2):
        for dataVal in range(0, 8):
            if (dCache[row][dataVal] == currVal):
                cacheHits += 1
                print(cacheHits)
                return False

    setAssociativeCache(currVal,data_value, displacement, isDouble)
    cacheHits += 1
    return True

def isaCacheMiss(data_value, displacement, isFirst, isDouble):
    global cacheHits
    if(isFirst == 0):
        regIndex = int(data_value[1:])
        currVal = register.R[regIndex] + displacement
        setAssociativeCache(currVal,data_value, displacement, isDouble)
        cacheHits += 1
        return True
    else:
        regIndex = int(data_value[1:])
        currVal = register.R[regIndex] + displacement
        if(isDouble == False):
            return search(currVal,data_value, displacement, isDouble)
        else:
            if(isDouble == True):
                return search(currVal+4,data_value, displacement, isDouble)

def setAssociativeCache(currVal,data_value,displacement, isDouble):
    global dCache
    regIndex = int(data_value[1:])
    word_address = currVal
    block_number = int(word_address/4)
    cache_word_address = block_number%4
    set_number = block_number%2

    if(cache_word_address == 1):
        var1 = word_address - 4
        var2 = var1+4
        var3 = var2+4
        var4 = var3+4

    if(cache_word_address == 2):
        var1 = word_address - 8
        var2 = word_address - 4
        var3 = word_address
        var4 = var3 + 4

    if(cache_word_address == 3):
        var1 = word_address - 12
        var2 = word_address - 8
        var3 = word_address - 4
        var4 = word_address

    if (cache_word_address == 0):
        var1 = word_address
        var2 = var1+4
        var3 = var2+4
        var4 = var3+4

    current = "current_MRU_None"
    if(dCache[set_number][0] == 0):
        dCache[set_number][0] = var1
        dCache[set_number][1] = var2
        dCache[set_number][2] = var3
        dCache[set_number][3] = var4
        current = 'current_MRU_'+str(set_number)+'_0'

    elif (dCache[set_number][4] == 0):
        dCache[set_number][4] = var1
        dCache[set_number][5] = var2
        dCache[set_number][6] = var3
        dCache[set_number][7] = var4
        current = 'current_MRU_'+str(set_number)+'_1'

    else:
        if(set_number == 0 and current == "current_MRU_0_0"):
            dCache[set_number][4] = var1
            dCache[set_number][5] = var2
            dCache[set_number][6] = var3
            dCache[set_number][7] = var4
            current = "current_MRU_0_1"
        elif(set_number == 0 and current == "current_MRU_0_1"):
            dCache[set_number][0] = var1
            dCache[set_number][1] = var2
            dCache[set_number][2] = var3
            dCache[set_number][3] = var4
            current = "current_MRU_0_0"
        elif(set_number == 1 and current == "current_MRU_1_0"):
            dCache[set_number][4] = var1
            dCache[set_number][5] = var2
            dCache[set_number][6] = var3
            dCache[set_number][7] = var4
            current = "current_MRU_1_1"
        elif(set_number == 1 and current == "current_MRU_1_1"):
            dCache[set_number][0] = var1
            dCache[set_number][1] = var2
            dCache[set_number][2] = var3
            dCache[set_number][3] = var4
            current = "current_MRU_1_0"

