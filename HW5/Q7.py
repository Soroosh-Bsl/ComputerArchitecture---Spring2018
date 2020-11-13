import datetime
import random


class cacheCell:
    data = 0
    tag = 0
    validity = False
    dirtiness = False


def isInCache(mainMemoryAddress):
    global cache
    address, tag = cacheAddressMap(mainMemoryAddress)
    if cache[address].tag == tag and cache[address].validity:
        return True, address
    elif cacheArch == 1 and cache[address + cacheSize//2].tag == tag and cache[address + cacheSize//2].validity:
        return True, address + cacheSize//2
    elif cacheArch == 2 and cache[address + cacheSize//4].tag == tag and cache[address + cacheSize//4].validity:
        return True, address + cacheSize//4
    elif cacheArch == 2 and cache[address + 2*cacheSize//4].tag == tag and cache[address + 2*cacheSize//4].validity:
        return True, address + 2*cacheSize//4
    elif cacheArch == 2 and cache[address + 3*cacheSize//4].tag == tag and cache[address + 3*cacheSize//4].validity:
        return True, address + 3*cacheSize//4
    return False, None


def cacheAddressMap(mainMemoryAddress):
    global cacheArch
    if cacheArch == 0:
        address = mainMemoryAddress % cacheSize
        tag = mainMemoryAddress//cacheSize
        return address, tag
    elif cacheArch == 1:
        numberOfSets = cacheSize//2
        address = mainMemoryAddress % numberOfSets
        tag = (mainMemoryAddress//numberOfSets)
        return address, tag
    else:
        numberOfSets = cacheSize // 4
        address = mainMemoryAddress % numberOfSets
        tag = (mainMemoryAddress // numberOfSets)
        return address, tag


def getToCache(mainMemoryAddress):
    global evictionType
    global cache
    address, tag = cacheAddressMap(mainMemoryAddress)
    if not cache[address].validity:
        return address
    elif cacheArch == 1 and not cache[address + cacheSize // 2].validity:
        return address + cacheSize // 2
    elif cacheArch == 2 and not cache[address + cacheSize // 4].validity:
        return address + cacheSize // 4
    elif cacheArch == 2 and not cache[address + 2 * cacheSize // 4].validity:
        return address + 2 * cacheSize // 4
    elif cacheArch == 2 and not cache[address + 3 * cacheSize // 4].validity:
        return address + 3 * cacheSize // 4
    else:
        evictedAdd, memoryADD = eviction(mainMemoryAddress, evictionType)
        return evictedAdd



def eviction(mainMemoryAddress, evictionType):
    if evictionType == 0:
        return evictionLRU(mainMemoryAddress)
    elif evictionType == 1:
        return evictionMRU(mainMemoryAddress)
    elif evictionType == 2:
        return evictionFIFO(mainMemoryAddress)
    elif evictionType == 3:
        return evictionRandom(mainMemoryAddress)


def evictionRandom(mainMemoryAddress):
    global cache
    address, tag = cacheAddressMap(mainMemoryAddress)
    if cacheArch == 0:
        cache[address].validity = False
        return address, address + cache[address].tag * cacheSize
    elif cacheArch == 1:
        randomNumber = random.randint(0, 1)
        address += randomNumber * cacheSize//2
        cache[address].validity = False
        return address, address + cache[address].tag * cacheSize // 2
    elif cacheArch == 2:
        randomNumber = random.randint(0, 3)
        address += randomNumber * cacheSize // 4
        cache[address].validity = False
        return address, address + cache[address].tag * cacheSize // 4


def evictionFIFO(mainMemoryAddress):
    global cache
    global timeCached
    address, tag = cacheAddressMap(mainMemoryAddress)
    reportAdd, reportAddF, reportAddF = 0, 0, 0
    if cacheArch == 0:
        cache[address].validity = False
        return address, address + cache[address].tag * cacheSize
    elif cacheArch == 1:
        if timeCached[address] < timeCached[address + cacheSize // 2]:
            cache[address + cacheSize // 2].validity = False
            return address + cacheSize // 2, address + cacheSize // 2 + cache[
                address + cacheSize // 2].tag * cacheSize // 2
        else:
            cache[address].validity = False
            return address, address + cache[address].tag * cacheSize // 2
    elif cacheArch == 2:
        if timeCached[address] < timeCached[address + cacheSize // 4]:
            reportAddF = address
        else:
            reportAddF = address + cacheSize // 4
        if timeCached[address + 2 * cacheSize // 4] < timeCached[address + 3 * cacheSize // 4]:
            reportAddS = address + 2 * cacheSize // 4
        else:
            reportAddS = address + 3 * cacheSize // 4
        if timeCached[reportAddF] < timeCached[reportAddS]:
            reportAdd = reportAddF
        else:
            reportAdd = reportAddS
        cache[reportAdd].validity = False
        return reportAdd, reportAdd + cache[reportAdd].tag * cacheSize // 4


def evictionMRU(mainMemoryAddress):
    global cache
    global timeUsed
    address, tag = cacheAddressMap(mainMemoryAddress)
    reportAdd, reportAddF, reportAddF = 0, 0, 0
    if cacheArch == 0:
        cache[address].validity = False
        return address, address + cache[address].tag * cacheSize
    elif cacheArch == 1:
        if timeUsed[address] < timeUsed[address + cacheSize // 2]:
            cache[address + cacheSize // 2].validity = False
            return address + cacheSize // 2, address + cacheSize // 2 + cache[
                address + cacheSize // 2].tag * cacheSize // 2
        else:
            cache[address].validity = False
            return address, address + cache[address].tag * cacheSize // 2
    elif cacheArch == 2:
        if timeUsed[address] < timeUsed[address + cacheSize // 4]:
            reportAddF = address
        else:
            reportAddF = address + cacheSize // 4
        if timeUsed[address + 2 * cacheSize // 4] < timeUsed[address + 3 * cacheSize // 4]:
            reportAddS = address + 2 * cacheSize // 4
        else:
            reportAddS = address + 3 * cacheSize // 4
        if timeUsed[reportAddF] < timeUsed[reportAddS]:
            reportAdd = reportAddF
        else:
            reportAdd = reportAddS
        cache[reportAdd].validity = False
        return reportAdd, reportAdd + cache[reportAdd].tag * cacheSize // 4


def evictionLRU(mainMemoryAddress):
    global cache
    global timeUsed
    address, tag = cacheAddressMap(mainMemoryAddress)
    reportAdd, reportAddF, reportAddF = 0, 0, 0
    if cacheArch == 0:
        cache[address].validity = False
        return address, address + cache[address].tag * cacheSize
    elif cacheArch == 1:
        if timeUsed[address] > timeUsed[address+cacheSize//2]:
            cache[address+cacheSize//2].validity = False
            return address+cacheSize//2, address+cacheSize//2+ cache[address+cacheSize//2].tag * cacheSize//2
        else:
            cache[address].validity = False
            return address, address + cache[address].tag * cacheSize//2
    elif cacheArch == 2:
        if timeUsed[address] > timeUsed[address+cacheSize//4]:
            reportAddF = address
        else:
            reportAddF = address+cacheSize//4
        if timeUsed[address+2*cacheSize//4] > timeUsed[address+3*cacheSize//4]:
            reportAddS = address+2*cacheSize//4
        else:
            reportAddS = address+3*cacheSize//4
        if timeUsed[reportAddF] > timeUsed[reportAddS]:
            reportAdd = reportAddF
        else:
            reportAdd = reportAddS
        cache[reportAdd].validity = False
        return reportAdd, reportAdd + cache[reportAdd].tag * cacheSize//4


def read(mainMemoryAddress):
    global cache
    global memory
    global hit
    global miss
    exist, address = isInCache(mainMemoryAddress)
    if exist:
        hit += 1
        timeUsed[address] = datetime.datetime.now()
        return cache[address].data
    else:
        miss += 1
        data = memory[mainMemoryAddress]
        address, tag = cacheAddressMap(mainMemoryAddress)
        address = getToCache(mainMemoryAddress)
        cache[address].data, cache[address].tag, cache[address].validity = data, tag, True
        timeUsed[address] = datetime.datetime.now()
        timeCached[address] = datetime.datetime.now()
        return data


def write(mainMemoryAddress, cacheEnable, data):
    global cache
    global memory
    global hit
    global miss
    exist, address = isInCache(mainMemoryAddress)

    if exist:
        hit += 1
        timeUsed[address] = datetime.datetime.now()
        cache[address].data, cache[address].dirtiness, cache[address].validity = data, True, True
        memory[mainMemoryAddress] = data
    else:
        miss += 1
        if cacheEnable:
            address, tag = cacheAddressMap(mainMemoryAddress)
            address = getToCache(mainMemoryAddress)
            cache[address].data, cache[address].tag, cache[address].validity, cache[address].dirtiness = data, tag, True, True
            timeUsed[address] = datetime.datetime.now()
            timeCached[address] = datetime.datetime.now()
            memory[mainMemoryAddress] = data
        else:
            memory[mainMemoryAddress] = data

cacheEnable = True

def bubbleSort():
    global memory
    for passnum in range(len(memory)-1,0,-1):
        for i in range(passnum):
            temp_one = read(i)
            temp_two = read(i+1)
            if temp_one > temp_two:
                write(i, cacheEnable, temp_two)
                write(i+1, cacheEnable, temp_one)


def insertionSort():
    global cacheEnable
    global memorySize
    for index in range(1,memorySize):
        currentvalue = read(index)
        position = index

        minus = read(position-1)
        while position > 0 and minus > currentvalue:
            write(position, cacheEnable, minus)
            position = position-1
            minus = read(position-1)
        write(position, cacheEnable, currentvalue)


def quickSort():
    global memorySize
    quickSortHelper(0,memorySize-1)

def quickSortHelper(first,last):
    if first<last:
        splitpoint = partition(first,last)

        quickSortHelper(first,splitpoint-1)
        quickSortHelper(splitpoint+1,last)


def partition(first,last):
    global cacheEnable
    pivotvalue = read(first)
    leftmark = first+1
    rightmark = last

    done = False
    while not done:

        leftValue = read(leftmark)
        while leftmark <= rightmark and leftValue <= pivotvalue and leftmark:
            leftmark = leftmark + 1
            if leftmark <= rightmark:
                leftValue = read(leftmark)

        rightValue = read(rightmark)
        while rightValue >= pivotvalue and rightmark >= leftmark:
            rightmark = rightmark -1
            if rightmark >= leftmark:
                rightValue = read(rightmark)


        if rightmark < leftmark:
            done = True
        else:
            write(leftmark, cacheEnable, rightValue)
            write(rightmark, cacheEnable, leftValue)

    temp = read(first)
    temp_sec = read(rightmark)
    write(first, cacheEnable, temp_sec)

    write(rightmark, cacheEnable, temp)
    return rightmark


def merge_sort():
    global cacheEnable
    global memorySize
    unit = 1
    while unit <= memorySize:
        print(unit)
        for h in range(0, memorySize, unit * 2):
            l, r = h, min(memorySize, h + 2 * unit)
            mid = h + unit
            p, q = l, mid
            while p < mid and q < r:
                first, second = read(p), read(q)
                if first < second:
                    p += 1
                else:
                    for i in range(q-1, p-1, -1):
                        temp = read(i)
                        write(i+1, cacheEnable, temp)
                    write(p, cacheEnable, second)
                    p, mid, q = p + 1, mid + 1, q + 1

        unit *= 2


cacheArch = 0
cacheSize = 100
timeUsed = [datetime.datetime.now()] * cacheSize
timeCached = [datetime.datetime.now()] * cacheSize
evictionType = 0#3#1#303#2####
miss = 0
hit = 0
memorySize = 10000
cache = [5] * cacheSize
for i in range(cacheSize):
    cache[i] = cacheCell()
memory = []

with open('data.txt') as f:
    for line in f:
        temp = line[:len(line)-1]
        memory.append(int(temp))

print("Before = ", memory)

# bubbleSort()
# insertionSort()
# quickSort()
merge_sort()

print("After = ", memory)
print("hits = ", hit)
print("miss = ", miss)