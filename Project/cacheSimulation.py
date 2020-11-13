import random
import sys
sys.setrecursionlimit(100000)

hits = 0
misses = 0
# mechanism is considered as write through
memorySize = 10000
cacheSize = 100

memory = list()
hits = 0
misses = 0

class CacheCell:
    def __init__(self, cacheArch):
        self.datas = [None for i in range(0 , pow(2 , cacheArch))]
        self.tags = [None for i in range(0 , pow(2 , cacheArch))]
        self.valids = [0 for i in range(0 , pow(2 , cacheArch))]
        self.dirties = [0 for i in range(0 , pow(2 , cacheArch))]
        self.LRUOrder = list()
        self.FIFOOrder = list()



class Cache:
    def __init__(self, cacheArch, writeType, evictType):
        self.cacheIndexNum = cacheSize // pow(2 , cacheArch)
        self.array = [CacheCell(cacheArch) for i in range(0 , cacheSize // pow(2 , cacheArch))]
        self.cacheArch = cacheArch
        self.writeType = writeType
        self.evictType = evictType # 0 -> LRU , 1 -> MRU , 2 -> FIFO , 3 -> Random , 4 -> BIP



    def cacheAddressMap(self, address):
        return address % self.cacheIndexNum

    def tagCalculate(self, address):
        return address // self.cacheIndexNum

    def isInCacheIndex(self, address):
        tag = self.tagCalculate(address)
        mappedAddress = self.cacheAddressMap(address)
        for i in range(pow(2 , self.cacheArch)):
            if self.array[mappedAddress].tags[i] == tag and self.array[mappedAddress].valids[i] == 1:
                return i
        return -1

    def isCacheIndexFull(self , index):
        for i in range(pow(2 , self.cacheArch)):
            if self.array[index].valids[i] == 0:
                return i
        return -1

    def writeInCache(self, address, amount):
        global hits,misses
        mappedIndex = self.cacheAddressMap(address)
        ID = self.isInCacheIndex(address)
        if ID != -1:
            hits += 1
            self.array[mappedIndex].datas[ID] = amount
            self.array[mappedIndex].tags[ID] = self.tagCalculate(address)
            self.array[mappedIndex].valids[ID] = 1
            self.array[mappedIndex].dirties[ID] = 1
            self.array[mappedIndex].LRUOrder.remove(ID)
            self.array[mappedIndex].LRUOrder.append(ID)
            return True
        else:
            misses += 1
            if self.isCacheIndexFull(mappedIndex) == -1:
                ID = self.eviction(mappedIndex)
                self.array[mappedIndex].datas[ID] = amount
                self.array[mappedIndex].tags[ID] = self.tagCalculate(address)
                self.array[mappedIndex].valids[ID] = 1
                self.array[mappedIndex].dirties[ID] = 0
                self.array[mappedIndex].LRUOrder.append(ID)
                self.array[mappedIndex].FIFOOrder.append(ID)
            else:
                ID = self.isCacheIndexFull(mappedIndex)
                self.array[mappedIndex].datas[ID] = amount
                self.array[mappedIndex].tags[ID] = self.tagCalculate(address)
                self.array[mappedIndex].valids[ID] = 1
                self.array[mappedIndex].dirties[ID] = 0
                self.array[mappedIndex].LRUOrder.append(ID)
                self.array[mappedIndex].FIFOOrder.append(ID)
            return False

    def readInCache(self, address):
        global hits, misses
        mappedIndex = self.cacheAddressMap(address)
        ID = self.isInCacheIndex(address)
        if ID != -1:
            hits += 1
            self.array[mappedIndex].datas[ID]
            self.array[mappedIndex].LRUOrder.remove(ID)
            self.array[mappedIndex].LRUOrder.append(ID)
            return True
        else:
            misses += 1
            return False

    def evictionLRU(self, index):
        cacheLine = self.array[index]
        removingId = cacheLine.LRUOrder.pop(0)
        cacheLine.FIFOOrder.remove(removingId)
        cacheLine.valids[removingId] = 0
        return removingId


    def evictionMRU(self, index):
        cacheLine = self.array[index]
        removingId = cacheLine.LRUOrder.pop(-1)
        cacheLine.FIFOOrder.remove(removingId)
        cacheLine.valids[removingId] = 0
        return removingId

    def evictionFIFO(self, index):
        cacheLine = self.array[index]
        removingId = cacheLine.FIFOOrder.pop(-1)
        cacheLine.LRUOrder.remove(removingId)
        cacheLine.valids[removingId] = 0
        return removingId

    def evictionRandom(self, index):
        cacheLine = self.array[index]
        removingId = random.randint(0 , len(cacheLine.LRUOrder) - 1)
        reID = cacheLine.LRUOrder[removingId]
        del cacheLine.LRUOrder[removingId]
        cacheLine.FIFOOrder.remove(reID)
        cacheLine.valids[reID] = 0
        return reID

    def evictionBIP(self, index , threshold): # respective policy is called BIP that is random between MRU and LRU!
        choice = random.uniform(0,1)
        if choice >= threshold:
            return self.evictionLRU(index)
        else:
            return self.evictionMRU(index)

    def eviction(self , index):
        if self.evictType == 0:
            return self.evictionLRU(index)
        elif self.evictType == 1:
            return self.evictionMRU(index)
        elif self.evictType == 2:
            return self.evictionFIFO(index)
        elif self.evictType == 3:
            return self.evictionRandom(index)
        else:
            return self.evictionBIP(index , 0.1)

    def invalidate(self, address):
        tag = self.tagCalculate(address)
        mappedAddress = self.cacheAddressMap(address)
        for i in range(pow(2, self.cacheArch)):
            if self.array[mappedAddress].tags[i] == tag and self.array[mappedAddress].valids[i] == 1:
                self.array[mappedAddress].valids[i] = 0
                return


def write(address, amount, cache):#type = 0 -> write around , type = 1 -> write allocate
    memory[address] = amount
    if cache.writeType == 1:
       return cache.writeInCache(address, amount)
    else:
        cache.invalidate(address)
        return False


def read(address, cache):
    amount = memory[address]
    result = cache.readInCache(address)
    if not result:
        cache.writeInCache(address, amount)
    return result

#
# def read_integers(filename):
#     with open(filename) as f:
#         return [int(x) for x in f]
#
#
# # recursive inplace MergeSort
# def mergeSortRec(a, b, cache):
#     if a == b:
#         return
#     mid = (a + b) // 2
#     mergeSort(a, mid, cache)
#     mergeSort(mid + 1, b, cache)
#     i, j = a, mid + 1
#     while i < j <= b:
#         # read(i, cache)
#         # read(j, cache)
#         # if arr[i] <= arr[j]:
#         if read(i, cache) <= read(j, cache):
#             i += 1
#             continue
#         else:
#             # temp = arr[j]
#             temp = read(j, cache)
#             for k in range(j - 1, i - 1, -1):
#                 write(k + 1, read(k, cache), cache)
#                 # arr[k + 1] = arr[k]
#             write(i, temp, cache)
#             # arr[i] = temp
#             i += 1
#             j += 1
#
#
# # usual inplace MergeSort
# def mergeSort(a, b, cache):
#     unit = 1
#     while unit <= b - a + 1:
#         h = 0
#         for h in range(a, b + 1, unit * 2):
#             l, r = h, min(b + 1, h + 2 * unit)
#             mid = h + unit
#             # merge xs[h:h + 2 * unit]
#             p, q = l, mid
#             while p < mid and q < r:
#                 if read(p, cache) < read(q, cache):
#                     p += 1
#                 else:
#                     tmp = read(q, cache)
#                     for k in range(q - 1, p - 1, -1):
#                         value = read(k, cache)
#                         write(k + 1, value, cache)
#                     write(p, tmp, cache)
#                     p, mid, q = p + 1, mid + 1, q + 1
#
#         unit *= 2
#
#
# def quickSort(a, b, cache):
#     if a >= b:
#         return
#     pivot = random.randint(a, b)
#     # pivotAmount = arr[pivot]
#     pivotAmount = read(pivot, cache)
#     i, j = a, b
#     while i <= pivot <= j:
#         # if arr[i] < pivotAmount:
#         if read(i, cache) < pivotAmount:
#             i += 1
#             continue
#         # elif arr[j] > pivotAmount:
#         elif read(j, cache) > pivotAmount:
#             j -= 1
#             continue
#         else:
#             # arr[i], arr[j] = arr[j], arr[i]
#             temp = read(i, cache)
#             write(i, read(j, cache), cache)
#             write(j, temp, cache)
#             if i == pivot:
#                 pivot = j
#                 j += 1
#             elif j == pivot:
#                 pivot = i
#                 i -= 1
#             i += 1
#             j -= 1
#     quickSort(a, pivot - 1, cache)
#     quickSort(pivot + 1, b, cache)
#
#
# def bubbleSort(a, b, cache):
#     for i in range(a, b):
#         for j in range(i, b + 1):
#             # if arr[i] > arr[j]:
#             if read(i, cache) > read(j, cache):
#                 # arr[i], arr[j] = arr[j], arr[i]
#                 temp = read(i, cache)
#                 write(i, read(j, cache), cache)
#                 write(j, temp, cache)
#
#
# def insertionSort(a, b, cache):
#     for i in range(a, b):
#         min = i
#         for j in range(i + 1, b + 1):
#             # if arr[j] < arr[min]:
#             if read(j, cache) < read(min, cache):
#                 min = j
#         # arr[i], arr[min] = arr[min], arr[i]
#         temp = read(min, cache)
#         write(min, read(j, cache), cache)
#         write(j, temp, cache)
#
#
# memory = read_integers("data.txt")
# consideringSize = 2000
# for wrType in range(0, 2):
#     for evicType in range(0, 5):
#         for arch in range(0, 3):
#             cache = Cache(arch, wrType, evicType)
#             misses = 0
#             hits = 0
#             mergeSort(0, consideringSize, cache)
#             print("mergeSort, cacheArch: " + str(arch) + ", writeType: " + str(wrType)
#                   + ", evictType: " + str(evicType) + "-> misses: " + str(misses) + ", hits: "
#                   + str(hits) + ", hit rate; " + str((hits / (hits + misses))))
#             cache = Cache(arch, wrType, evicType)
#             misses = 0
#             hits = 0
#             quickSort(0, consideringSize, cache)
#             print("quickSort, cacheArch: " + str(arch) + ", writeType: " + str(wrType)
#                   + ", evictType: " + str(evicType) + "-> misses: " + str(misses) + ", hits: "
#                   + str(hits) + ", hit rate; " + str((hits / (hits + misses))))
#             cache = Cache(arch, wrType, evicType)
#             misses = 0
#             hits = 0
#             bubbleSort(0, consideringSize, cache)
#             print("bubbleSort, cacheArch: " + str(arch) + ", writeType: " + str(wrType)
#                   + ", evictType: " + str(evicType) + "-> misses: " + str(misses) + ", hits: "
#                   + str(hits) + ", hit rate; " + str((hits / (hits + misses))))
#             cache = Cache(arch, wrType, evicType)
#             misses = 0
#             hits = 0
#             insertionSort(0, consideringSize, cache)
#             print("insertionSort, cacheArch: " + str(arch) + ", writeType: " + str(wrType)
#                   + ", evictType: " + str(evicType) + "-> misses: " + str(misses) + ", hits: "
#                   + str(hits) + ", hit rate; " + str((hits / (hits + misses))))

# cache = Cache(2, 0, 2)
# write(10 , 1000, cache)
# read(10 , cache)
# write(110 , 2000 , cache)
# read(110 , cache)
# read(10 , cache)
# mergeSort(0, 2000, cache)
# quickSort(0, len(memory) - 1, cache)
# bubbleSort(0, 999, cache)
# insertionSort(0, 2000, cache)
# print(memory)
# print(misses)
# print(hits)


# arr = [8, 10, 9, 3, 22, 8, 9, -2, 12, 134]
# insertionSort(arr, 0, 9)
# print(arr)
# bubbleSort(memory, 0, 9999)
# print(memory)
# quickSort(memory, 0, len(memory) - 1)
# print(memory)
# mergeSort(memory , 0 , len(memory) - 1)
# print(memory)









