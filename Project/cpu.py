import random

import copy

import cacheSimulation as Cache
import sys

sys.setrecursionlimit(1000000)
total_delay = 0

cache = None
sim = None
Cache.memorySize, Cache.cacheSize = 5, 5
cacheArch, writeType, evictType = 5, 5, 5

class Register:
    def __init__(self, name, numOfBits, shiftLeftAmount, arithmeticOp, ID):
        self.name = name
        self.bitSize = numOfBits
        self.shiftLeftAmount = shiftLeftAmount
        self.arithmeticOp = arithmeticOp
        self.amount = 0
        self.signals = list()
        self.initializeSignals()
        self.ID = ID

    def setAmount(self, amount):
        if amount > 0:
            self.amount = amount % (pow(2, self.bitSize))
        else:
            self.amount = - ((-amount) % (pow(2, self.bitSize)+1))
    def fixAmount(self):
        if self.amount > 0:
            self.amount = self.amount % (pow(2, self.bitSize))
        else:
            self.amount = - ((-self.amount) % (pow(2, self.bitSize)+1))

    def getBusAmount(self):
        self.fixAmount()
        return self.amount * pow(2, self.shiftLeftAmount)

    def initializeSignals(self):
        clearSyn = Signal(self.name, "clearSyn")
        self.signals.append(clearSyn)
        clearAsyn = Signal(self.name, "clearAsyn")
        self.signals.append(clearAsyn)
        if self.name == "OffsetR":
            loadUp = Signal(self.name, "loadUp")
            self.signals.append(loadUp)
            loadDown = Signal(self.name, "loadDown")
            self.signals.append(loadDown)
        else:
            load = Signal(self.name, "load")
            self.signals.append(load)
        if self.arithmeticOp:
            inc = Signal(self.name, "inc")
            self.signals.append(inc)
            dec = Signal(self.name, "dec")
            self.signals.append(dec)
            inc4 = Signal(self.name, "inc4")
            self.signals.append(inc4)
            dec4 = Signal(self.name, "dec4")
            self.signals.append(dec4)

    def getName(self):
        return "Register " + self.name


class Flip_flap:
    def __init__(self, name):
        self.name = name
        self.amount = 0
        self.signals = list()


class Flip_flap_RS(Flip_flap):
    def __init__(self, name):
        Flip_flap.__init__(self, name)
        self.initializeSignals()

    def initializeSignals(self):
        S = Signal(self.name, "S")
        self.signals.append(S)
        R = Signal(self.name, "R")
        self.signals.append(R)

    def getName(self):
        return "Flip-flap RS " + self.name


class Flip_flap_T(Flip_flap):
    def __init__(self, name):
        Flip_flap.__init__(self, name)
        self.initializeSignals()

    def initializeSignals(self):
        T = Signal(self.name, "T")
        self.signals.append(T)

    def getName(self):
        return "Flip-flap T " + self.name


class Signal:
    def __init__(self, moduleName, operation):
        self.moduleName = moduleName
        self.operation = operation
        self.amount = 0

    def getName(self):
        return "Signal " + self.moduleName + " " + self.operation


def binTwoCompSystem(n, bits):
    s = bin(n & int("1" * bits, 2))[2:]
    return ("{0:0>%s}" % bits).format(s)


class Memory:
    def __init__(self, size):
        self.size = size
        self.array = [0] * size
        self.strings = ["0000"] * size
        self.signals = list()
        self.initializeSignals()
        return

    def initializeSignals(self):
        MemRead = Signal("Memory", "MemRead")
        self.signals.append(MemRead)
        MemWrite = Signal("Memory", "MemWrite")
        self.signals.append(MemWrite)

    def readInstr(self, address):
        if address >= self.size:
            raise Exception("Memory Size Limit Reached")
        if not Cache.read(address, cache):
            delay = random.randint(1, 5)
        else:
            delay = 1
        return self.array[address], delay

    def readData(self, address):
        if address + 3 >= self.size:
            raise Exception("Memory Size Limit Reached")
        if not Cache.read(address, cache):
            delay = random.randint(1, 5)
        else:
            delay = 1
        return self.array[address], delay

    def writeInstr(self, address, amount):
        if address >= self.size:
            raise Exception("Memory Size Limit Reached")

        if not Cache.write(address, amount, cache):
            delay = random.randint(1, 5)
        else:
            delay = 1
        # self.array[address] = amount
        self.strings[address] = binTwoCompSystem(amount, 8)
        return delay

    def writeData(self, address, amount):
        if address + 3 >= self.size:
            raise Exception("Memory Size Limit Reached")

        if not Cache.write(address, amount, cache):
            delay = random.randint(1, 5)
        else:
            delay = 1
        Cache.write(address + 1, amount, cache)
        Cache.write(address + 2, amount, cache)
        Cache.write(address + 3, amount, cache)
        # self.array[address] = amount
        # self.array[address + 1] = amount
        # self.array[address + 2] = amount
        # self.array[address + 3] = amount
        amount = binTwoCompSystem(amount, 32)
        self.strings[address] = amount[0:8]
        self.strings[address + 1] = amount[8:16]
        self.strings[address + 2] = amount[16:24]
        self.strings[address + 3] = amount[24:32]

        return delay


def initialize():
    registers = list()
    signals = list()
    memory = Memory(1000)
    signals.extend(memory.signals)
    flip_flaps = list()

    AdR = Register("AdR", 32, 0, True, 1)
    registers.append(AdR)
    signals.extend(AdR.signals)
    PC = Register("PC", 32, 0, True, 2)
    registers.append(PC)
    signals.extend(PC.signals)
    CPP = Register("CPP", 32, 0, True, 3)
    registers.append(CPP)
    signals.extend(CPP.signals)
    LV = Register("LV", 32, 0, True, 4)
    registers.append(LV)
    signals.extend(LV.signals)
    SP = Register("SP", 32, 0, True, 5)
    registers.append(SP)
    signals.extend(SP.signals)
    IR = Register("IR", 8, 0, False, 6)
    registers.append(IR)
    signals.extend(IR.signals)
    ByteR = Register("ByteR", 8, 0, False, 7)
    registers.append(ByteR)
    signals.extend(ByteR.signals)
    ConstR = Register("ConstR", 8, 0, False, 8)
    registers.append(ConstR)
    signals.extend(ConstR.signals)
    VarnumR = Register("VarnumR", 8, 2, False, 9)
    registers.append(VarnumR)
    signals.extend(VarnumR.signals)
    OffsetR = Register("OffsetR", 16, 0, False, 10)
    registers.append(OffsetR)
    signals.extend(OffsetR.signals)
    DR1 = Register("DR1", 32, 0, False, 11)
    registers.append(DR1)
    signals.extend(DR1.signals)
    OutR = Register("OutR", 32, 0, False, 12)
    registers.append(OutR)
    signals.extend(OutR.signals)
    DR2 = Register("DR2", 32, 0, False, 13)
    registers.append(DR2)
    signals.extend(DR2.signals)
    TR = Register("TR", 32, 0, True, 14)
    registers.append(TR)
    signals.extend(TR.signals)

    S = Flip_flap_RS("S")
    flip_flaps.append(S)
    signals.extend(S.signals)
    Z = Flip_flap_RS("Z")
    flip_flaps.append(Z)
    signals.extend(Z.signals)
    N = Flip_flap_RS("N")
    flip_flaps.append(N)
    signals.extend(N.signals)
    Enable_N = Flip_flap_T("Enable_N")
    flip_flaps.append(Enable_N)
    signals.extend(Enable_N.signals)
    Enable_Z = Flip_flap_T("Enable_Z")
    flip_flaps.append(Enable_Z)
    signals.extend(Enable_Z.signals)
    return registers, signals, memory, flip_flaps


Registers, Signals, Memory, Flip_flaps = initialize()
# ALUSignals = ""
# ALUOp = ""
# BUSSignal = ""
# BUSReg = ""


def setALUSignals(ALUOp):
    if ALUOp == "Add":
        return "111100"
    elif ALUOp == "Sub":
        return "111111"
    else:
        return "000000"


def setBusSignals(BUSReg):
    return "{0:b}".format(BUSReg).zfill(4)


def setSignal(signals, moduleName, operation, amount):
    for i in signals:
        if i.moduleName == moduleName and i.operation == operation:
            i.amount = amount
            return
    raise Exception("Signal Name is missMatched")


def resetSignals(signals):
    for i in signals:
        i.amount = 0


def getRegister(registers, name):
    for i in registers:
        if i.name == name:
            return i
    raise Exception("Register Name is missMatched")


def getFlip_Flap(flipflaps, name):
    for i in flipflaps:
        if i.name == name:
            return i
    raise Exception("Flip_Flap Name is missMatched")


def moveRegister(registers, source, destination, signals):
    tmp = getRegister(registers, destination)
    tmp.setAmount(getRegister(registers, source).getBusAmount())
    setSignal(signals, destination, "load", 1)
    return setBusSignals(getRegister(registers, source).ID)


def arithmeticOpRegister(registers, source, change, signals):
    tmpReg = getRegister(registers, source)
    tmpAmount = tmpReg.amount
    tmpReg.setAmount(tmpAmount + change)
    operation = ""
    if change == 1:
        operation = "inc"
    elif change == 4:
        operation = "inc4"
    elif change == -1:
        operation = "dec1"
    elif change == -4:
        operation = "dec4"
    setSignal(signals, source, operation, 1)


def ALUOperation(registers, ALUOp, signals, flip_flaps):
    if ALUOp == "Add":
        getRegister(registers, "OutR").setAmount(getRegister(registers, "DR1").amount + getRegister(registers, "DR2").amount)
        setSignal(signals, "OutR", "load", 1)
    elif ALUOp == "Sub":
        getRegister(registers, "OutR").setAmount(getRegister(registers, "DR2").amount - getRegister(registers, "DR1").amount)
        setSignal(signals, "OutR", "load", 1)
    elif ALUOp == "A":
        getRegister(registers, "OutR").setAmount(getRegister(registers, "DR1").amount)
        setSignal(signals, "OutR", "load", 1)
    if getFlip_Flap(flip_flaps, "Enable_N").amount == 0:
        if getRegister(registers, "OutR").amount < 0:
            getFlip_Flap(flip_flaps, "N").amount = 1
            setSignal(signals, "N", "S", 1)
        else:
            getFlip_Flap(flip_flaps, "N").amount = 0
            setSignal(signals, "N", "R", 1)
    if getFlip_Flap(flip_flaps, "Enable_Z").amount == 0:
        if getRegister(registers, "OutR").amount == 0:
            getFlip_Flap(flip_flaps, "Z").amount = 1
            setSignal(signals, "Z", "S", 1)
        else:
            getFlip_Flap(flip_flaps, "Z").amount = 0
            setSignal(signals, "Z", "R", 1)
    return setALUSignals(ALUOp)


def readInstrFromMemory(registers, destination, memory, signals):
    getRegister(registers, destination).amount, clocks = memory.readInstr(getRegister(registers, "AdR").amount)
    getRegister(registers, destination).fixAmount()
    setSignal(signals, destination, "load", 1)
    setSignal(signals, "Memory", "MemRead", 1)
    return setBusSignals(0), clocks


def readInstrFromMemoryToOffset(registers, up, memory, signals):
    if up:
        tmpAmount, clocks = memory.readInstr(getRegister(registers, "AdR").amount)
        tmpReg = getRegister(registers, "OffsetR")
        bagh = (tmpReg.amount % pow(2, tmpReg.bitSize // 2)) if tmpReg.amount >= 0 else (tmpReg.amount % pow(2, tmpReg.bitSize // 2)-pow(2, tmpReg.bitSize // 2))
        tmpReg.setAmount(bagh + pow(2, tmpReg.bitSize // 2) * tmpAmount)
        setSignal(signals, "OffsetR", "loadUp", 1)
        setSignal(signals, "Memory", "MemRead", 1)
    else:
        tmpAmount, clocks = memory.readInstr(getRegister(registers, "AdR").amount)
        tmpReg = getRegister(registers, "OffsetR")
        bagh = (tmpReg.amount % pow(2, tmpReg.bitSize)) if tmpReg.amount >= 0 else (tmpReg.amount % pow(2, tmpReg.bitSize)-pow(2, tmpReg.bitSize))
        tmpReg.setAmount(tmpReg.amount - bagh + tmpAmount)
        setSignal(signals, "OffsetR", "loadDown", 1)
        setSignal(signals, "Memory", "MemRead", 1)
    return setBusSignals(0), clocks


def readDataFromMemory(registers, destination, memory, signals):
    getRegister(registers, destination).amount, clocks = memory.readData(getRegister(registers, "AdR").amount)
    getRegister(registers, destination).fixAmount()
    setSignal(signals, destination, "load", 1)
    setSignal(signals, "Memory", "MemRead", 1)
    return setBusSignals(0), clocks


def writeInstrToMemory(registers, source, memory, signals):
    clocks = memory.writeInstr(getRegister(registers, "AdR").amount, getRegister(registers, source).getBusAmount())
    setSignal(signals, "Memory", "MemWrite", 1)
    return setBusSignals(getRegister(registers, source).ID), clocks


def writeDataToMemory(registers, source, memory, signals):

    clocks = memory.writeData(getRegister(registers, "AdR").amount, getRegister(registers, source).getBusAmount())
    setSignal(signals, "Memory", "MemWrite", 1)
    return setBusSignals(getRegister(registers, source).ID), clocks


class Instruction:
    def __init__(self, line, name, ID, demandingClocks, registers, signals, memory, flip_flaps):
        self.line = line
        self.name = name
        self.ID = ID
        self.demandingClocks = demandingClocks
        self.SC = 0# Sequence Counter
        self.registers = registers
        self.signals = signals
        self.memory = memory
        self.BUSSignals = "1111"
        self.ALUSignals = "000000"
        self.flip_flaps = flip_flaps
        self.done = False

    def stepForward(self):
        resetSignals(self.signals)
        delay = 1
        if self.SC == 0:
            delay += self.stepForward0()
        elif self.SC == 1:
            delay += self.stepForward1()
        if self.name == "IADD":
            if self.SC == 2:
                self.BUSSignals = moveRegister(self.registers, "SP", "AdR", self.signals)
                arithmeticOpRegister(self.registers, "SP", -4, self.signals)
            elif self.SC == 3:
                self.BUSSignals, clocks = readDataFromMemory(self.registers, "DR1", self.memory, self.signals)
                arithmeticOpRegister(self.registers, "AdR", -4, self.signals)
                delay += clocks
            elif self.SC == 4:
                self.BUSSignals, clocks = readDataFromMemory(self.registers, "DR2", self.memory, self.signals)
                delay += clocks
            elif self.SC == 5:
                self.ALUSignals = ALUOperation(self.registers, "Add", self.signals, self.flip_flaps)
            elif self.SC == 6:
                writeDataToMemory(self.registers, "OutR", self.memory, self.signals)
                self.done = True
        elif self.name == "ISUB":
            if self.SC == 2:
                self.BUSSignals = moveRegister(self.registers, "SP", "AdR", self.signals)
                arithmeticOpRegister(self.registers, "SP", -4, self.signals)
            elif self.SC == 3:
                self.BUSSignals, clocks = readDataFromMemory(self.registers, "DR2", self.memory, self.signals)
                arithmeticOpRegister(self.registers, "AdR", -4, self.signals)
                delay += clocks
            elif self.SC == 4:
                self.BUSSignals, clocks = readDataFromMemory(self.registers, "DR1", self.memory, self.signals)
                delay += clocks
            elif self.SC == 5:
                self.ALUSignals = ALUOperation(self.registers, "Sub", self.signals, self.flip_flaps)
            elif self.SC == 6:
                writeDataToMemory(self.registers, "OutR", self.memory, self.signals)
                self.done = True
        elif self.name == "NOP":
            if self.SC == 2:
                self.done = True
        elif self.name == "GOTO":
            if self.SC == 2:
                self.BUSSignals = moveRegister(self.registers, "PC", "AdR", self.signals)
                arithmeticOpRegister(self.registers, "PC", 1, self.signals)
            elif self.SC == 3:
                self.BUSSignals, clocks = readInstrFromMemoryToOffset(self.registers, True, self.memory, self.signals)
                arithmeticOpRegister(self.registers, "AdR", 1, self.signals)
                delay += clocks
            elif self.SC == 4:
                self.BUSSignals, clocks = readInstrFromMemoryToOffset(self.registers, False, self.memory, self.signals)
                arithmeticOpRegister(self.registers, "PC", 1, self.signals)
                delay += clocks
            elif self.SC == 5:
                self.BUSSignals = moveRegister(self.registers, "OffsetR", "DR1", self.signals)
            elif self.SC == 6:
                self.BUSSignals = moveRegister(self.registers, "PC", "DR2", self.signals)
            elif self.SC == 7:
                self.ALUSignals = ALUOperation(self.registers, "Add", self.signals, self.flip_flaps)
            elif self.SC == 8:
                self.BUSSignals = moveRegister(self.registers, "OutR", "PC", self.signals)
                self.done = True
        elif self.name == "IFEQ":
            if self.SC == 2:
                self.BUSSignals = moveRegister(self.registers, "PC", "AdR", self.signals)
                arithmeticOpRegister(self.registers, "PC", 1, self.signals)
            elif self.SC == 3:
                self.BUSSignals, clocks = readInstrFromMemoryToOffset(self.registers, True, self.memory, self.signals)
                arithmeticOpRegister(self.registers, "AdR", 1, self.signals)
                delay += clocks
            elif self.SC == 4:
                self.BUSSignals, clocks = readInstrFromMemoryToOffset(self.registers, False, self.memory, self.signals)
                arithmeticOpRegister(self.registers, "PC", 1, self.signals)
                delay += clocks
            elif self.SC == 5:
                self.BUSSignals = moveRegister(self.registers, "SP", "AdR", self.signals)
                arithmeticOpRegister(self.registers, "SP", -4, self.signals)
            elif self.SC == 6:
                self.BUSSignals, clocks = readDataFromMemory(self.registers, "DR1", self.memory, self.signals)
                delay += clocks
            elif self.SC == 7:
                self.ALUSignals = ALUOperation(self.registers, "A", self.signals, self.flip_flaps)
            elif self.SC == 8 and getFlip_Flap(self.flip_flaps, "Z").amount == 1:
                getFlip_Flap(self.flip_flaps, "Enable_Z").amount = 1
                setSignal(self.signals, "Enable_Z", "T", 1)
                self.BUSSignals = moveRegister(self.registers, "PC", "DR1", self.signals)
            elif self.SC == 9 and getFlip_Flap(self.flip_flaps, "Z").amount == 1:
                self.BUSSignals = moveRegister(self.registers, "OffsetR", "DR2", self.signals)
            elif self.SC == 10 and getFlip_Flap(self.flip_flaps, "Z").amount == 1:
                self.ALUSignals = ALUOperation(self.registers, "Add", self.signals, self.flip_flaps)
            elif self.SC == 11:
                if getFlip_Flap(self.flip_flaps, "Z").amount == 1:
                    self.BUSSignals = moveRegister(self.registers, "OutR", "PC", self.signals)
                    getFlip_Flap(self.flip_flaps, "Enable_Z").amount = 0
                    setSignal(self.signals, "Enable_Z", "T", 1)
                self.done = True
        elif self.name == "IFLT":
            if self.SC == 2:
                self.BUSSignals = moveRegister(self.registers, "PC", "AdR", self.signals)
                arithmeticOpRegister(self.registers, "PC", 1, self.signals)
            elif self.SC == 3:
                self.BUSSignals, clocks = readInstrFromMemoryToOffset(self.registers, True, self.memory, self.signals)
                arithmeticOpRegister(self.registers, "AdR", 1, self.signals)
                delay += clocks
            elif self.SC == 4:
                self.BUSSignals, clocks = readInstrFromMemoryToOffset(self.registers, False, self.memory, self.signals)
                arithmeticOpRegister(self.registers, "PC", 1, self.signals)
                delay += clocks
            elif self.SC == 5:
                self.BUSSignals = moveRegister(self.registers, "SP", "AdR", self.signals)
                arithmeticOpRegister(self.registers, "SP", -4, self.signals)
            elif self.SC == 6:
                self.BUSSignals, clocks = readDataFromMemory(self.registers, "DR1", self.memory, self.signals)
                delay += clocks
            elif self.SC == 7:
                self.ALUSignals = ALUOperation(self.registers, "A", self.signals, self.flip_flaps)
            elif self.SC == 8 and getFlip_Flap(self.flip_flaps, "N").amount == 1:
                getFlip_Flap(self.flip_flaps, "Enable_N").amount = 1
                setSignal(self.signals, "Enable_N", "T", 1)
                self.BUSSignals = moveRegister(self.registers, "PC", "DR1", self.signals)
            elif self.SC == 9 and getFlip_Flap(self.flip_flaps, "N").amount == 1:
                self.BUSSignals = moveRegister(self.registers, "OffsetR", "DR2", self.signals)
            elif self.SC == 10 and getFlip_Flap(self.flip_flaps, "N").amount == 1:
                self.ALUSignals = ALUOperation(self.registers, "Add", self.signals, self.flip_flaps)
            elif self.SC == 11:
                if getFlip_Flap(self.flip_flaps, "N").amount == 1:
                    self.BUSSignals = moveRegister(self.registers, "OutR", "PC", self.signals)
                    getFlip_Flap(self.flip_flaps, "Enable_N").amount = 0
                    setSignal(self.signals, "Enable_N", "T", 1)
                self.done = True
        elif self.name == "IF_ICMPEQ":
            if self.SC == 2:
                self.BUSSignals = moveRegister(self.registers, "PC", "AdR", self.signals)
                arithmeticOpRegister(self.registers, "PC", 1, self.signals)
            elif self.SC == 3:
                self.BUSSignals, clocks = readInstrFromMemoryToOffset(self.registers, True, self.memory, self.signals)
                arithmeticOpRegister(self.registers, "AdR", 1, self.signals)
                delay += clocks
            elif self.SC == 4:
                self.BUSSignals, clocks = readInstrFromMemoryToOffset(self.registers, False, self.memory, self.signals)
                arithmeticOpRegister(self.registers, "PC", 1, self.signals)
                delay += clocks
            elif self.SC == 5:
                self.BUSSignals = moveRegister(self.registers, "SP", "AdR", self.signals)
                arithmeticOpRegister(self.registers, "SP", -4, self.signals)
            elif self.SC == 6:
                self.BUSSignals, clocks = readDataFromMemory(self.registers, "DR1", self.memory, self.signals)
                arithmeticOpRegister(self.registers, "SP", -4, self.signals)
                arithmeticOpRegister(self.registers, "AdR", -4, self.signals)
                delay += clocks
            elif self.SC == 7:
                self.BUSSignals, clocks = readDataFromMemory(self.registers, "DR2", self.memory, self.signals)
                delay += clocks
            elif self.SC == 8:
                self.ALUSignals = ALUOperation(self.registers, "Sub", self.signals, self.flip_flaps)
            elif self.SC == 9 and getFlip_Flap(self.flip_flaps, "Z").amount == 1:
                getFlip_Flap(self.flip_flaps, "Enable_Z").amount = 1
                setSignal(self.signals, "Enable_Z", "T", 1)
                self.BUSSignals = moveRegister(self.registers, "PC", "DR1", self.signals)
            elif self.SC == 10 and getFlip_Flap(self.flip_flaps, "Z").amount == 1:
                self.BUSSignals = moveRegister(self.registers, "OffsetR", "DR2", self.signals)
            elif self.SC == 11 and getFlip_Flap(self.flip_flaps, "Z").amount == 1:
                self.ALUSignals = ALUOperation(self.registers, "Add", self.signals, self.flip_flaps)
            elif self.SC == 12:
                if getFlip_Flap(self.flip_flaps, "Z").amount == 1:
                    self.BUSSignals = moveRegister(self.registers, "OutR", "PC", self.signals)
                    getFlip_Flap(self.flip_flaps, "Enable_Z").amount = 0
                    setSignal(self.signals, "Enable_Z", "T", 1)
                self.done = True
        elif self.name == "BIPUSH":
            if self.SC == 2:
                self.BUSSignals = moveRegister(self.registers, "PC", "AdR", self.signals)
                arithmeticOpRegister(self.registers, "PC", 1, self.signals)
            elif self.SC == 3:
                self.BUSSignals, clocks = readInstrFromMemory(self.registers, "ByteR", self.memory, self.signals)
                arithmeticOpRegister(self.registers, "SP", 4, self.signals)
                delay += clocks
            elif self.SC == 4:
                self.BUSSignals = moveRegister(self.registers, "SP", "AdR", self.signals)
            elif self.SC == 5:
                self.BUSSignals, clocks = writeDataToMemory(self.registers, "ByteR", self.memory, self.signals)
                delay += clocks
                self.done = True
        elif self.name == "ILOAD":
            if self.SC == 2:
                self.BUSSignals = moveRegister(self.registers, "PC", "AdR", self.signals)
                arithmeticOpRegister(self.registers, "PC", 1, self.signals)
            elif self.SC == 3:
                self.BUSSignals, clocks = readInstrFromMemory(self.registers, "VarnumR", self.memory, self.signals)
                delay += clocks
            elif self.SC == 4:
                self.BUSSignals = moveRegister(self.registers, "VarnumR", "DR1", self.signals)
            elif self.SC == 5:
                self.BUSSignals = moveRegister(self.registers, "LV", "DR2", self.signals)
            elif self.SC == 6:
                self.ALUSignals = ALUOperation(self.registers, "Add", self.signals, self.flip_flaps)
                arithmeticOpRegister(self.registers, "SP", 4, self.signals)
            elif self.SC == 7:
                self.BUSSignals = moveRegister(self.registers, "OutR", "AdR", self.signals)
            elif self.SC == 8:
                self.BUSSignals, clocks = readDataFromMemory(self.registers, "TR", self.memory, self.signals)
                delay += clocks
            elif self.SC == 9:
                self.BUSSignals = moveRegister(self.registers, "SP", "AdR", self.signals)
            elif self.SC == 10:
                self.BUSSignals, clocks = writeDataToMemory(self.registers, "TR", self.memory, self.signals)
                delay += clocks
                self.done = True
        elif self.name == "ISTORE":
            if self.SC == 2:
                self.BUSSignals = moveRegister(self.registers, "PC", "AdR", self.signals)
                arithmeticOpRegister(self.registers, "PC", 1, self.signals)
            elif self.SC == 3:
                self.BUSSignals, clocks = readInstrFromMemory(self.registers, "VarnumR", self.memory, self.signals)
                delay += clocks
            elif self.SC == 4:
                self.BUSSignals = moveRegister(self.registers, "SP", "AdR", self.signals)
                arithmeticOpRegister(self.registers, "SP", -4, self.signals)
            elif self.SC == 5:
                self.BUSSignals, clocks = readDataFromMemory(self.registers, "TR", self.memory, self.signals)
                delay += clocks
            elif self.SC == 6:
                self.BUSSignals = moveRegister(self.registers, "VarnumR", "DR1", self.signals)
            elif self.SC == 7:
                self.BUSSignals = moveRegister(self.registers, "LV", "DR2", self.signals)
            elif self.SC == 8:
                self.ALUSignals = ALUOperation(self.registers, "Add", self.signals, self.flip_flaps)
            elif self.SC == 9:
                self.BUSSignals = moveRegister(self.registers, "OutR", "AdR", self.signals)
            elif self.SC == 10:
                self.BUSSignals, clocks = writeDataToMemory(self.registers, "TR", self.memory, self.signals)
                delay += clocks
                self.done = True
        elif self.name == "IINC":
            if self.SC == 2:
                self.BUSSignals = moveRegister(self.registers, "PC", "AdR", self.signals)
                arithmeticOpRegister(self.registers, "PC", 1, self.signals)
            elif self.SC == 3:
                self.BUSSignals, clocks = readInstrFromMemory(self.registers, "VarnumR", self.memory, self.signals)
                arithmeticOpRegister(self.registers, "AdR", 1, self.signals)
                delay += clocks
            elif self.SC == 4:
                self.BUSSignals, clocks = readInstrFromMemory(self.registers, "ConstR", self.memory, self.signals)
                arithmeticOpRegister(self.registers, "PC", 1, self.signals)
                delay += clocks
            elif self.SC == 5:
                self.BUSSignals = moveRegister(self.registers, "VarnumR", "DR1", self.signals)
            elif self.SC == 6:
                self.BUSSignals = moveRegister(self.registers, "LV", "DR2", self.signals)
            elif self.SC == 7:
                self.ALUSignals = ALUOperation(self.registers, "Add", self.signals, self.flip_flaps)
            elif self.SC == 8:
                self.BUSSignals = moveRegister(self.registers, "OutR", "AdR", self.signals)
            elif self.SC == 9:
                self.BUSSignals, clocks = readDataFromMemory(self.registers, "DR1", self.memory, self.signals)
                delay += clocks
            elif self.SC == 10:
                self.BUSSignals = moveRegister(self.registers, "ConstR", "DR2", self.signals)
            elif self.SC == 11:
                self.ALUSignals = ALUOperation(self.registers, "Add", self.signals, self.flip_flaps)
            elif self.SC == 12:
                self.BUSSignals, clocks = writeDataToMemory(self.registers, "OutR", self.memory, self.signals)
                delay += clocks
                self.done = True

        self.SC += 1
        return delay, self.done

    def stepForward0(self):
        self.BUSSignals = moveRegister(self.registers, "PC", "AdR", self.signals)
        return 0

    def stepForward1(self):
        self.BUSSignals, clocks = readInstrFromMemory(self.registers, "IR", self.memory, self.signals)
        arithmeticOpRegister(self.registers, "PC", 1, self.signals)
        return clocks



# import test_graphic
# # test_graphic.
# test_graphic.start()
# file = None
# print("please enter PC, SP, LV and CPP respectively")
# while test_graphic.sim == None:
# time.sleep(10)


# getRegister(Registers, "PC").amount, getRegister(Registers, "SP").amount, getRegister(Registers, "LV").amount,\
# getRegister(Registers, "CPP").amount = test_graphic.pc, test_graphic.sp, test_graphic.lv, test_graphic.cpp
#
# Cache.memorySize, Cache.cacheSize = len(Memory.array), test_graphic.size
# cacheArch, writeType, evictType = test_graphic.arch, test_graphic.write, test_graphic.evict
#
# cache = Cache.Cache(cacheArch, writeType, evictType)
# Cache.memory = Memory.array
#
# file = test_graphic.file


file = None

def do():
    global total_delay
    global file
    # file = file
    line = file.readline()
    temp_pc = getRegister(Registers, "PC").amount
    print(temp_pc)
    inst_gam = 1
    dat_gam = 4

    while line:
        print(Memory.array)
        command = list(line.split())
        if command[0] == "HLT":
            Memory.writeInstr(temp_pc, 1000)
        if command[0] == "ORG":
            temp_pc = int(command[1])
            line = file.readline()
            continue
        if len(command) == 1:
            if command[0] == "NOP":
                Memory.writeInstr(temp_pc, 0)
                temp_pc += inst_gam
            elif command[0] == "IADD":
                Memory.writeInstr(temp_pc, 96)
                temp_pc += inst_gam
            elif command[0] == "ISUB":
                Memory.writeInstr(temp_pc, 100)
                temp_pc += inst_gam
        elif len(command) == 2:
            if command[0] == "BIPUSH":
                Memory.writeInstr(temp_pc, 16)
                temp_pc += inst_gam
                Memory.writeInstr(temp_pc, int(command[1]))
                temp_pc += inst_gam
            elif command[0] == "GOTO":
                Memory.writeInstr(temp_pc, 167)
                temp_pc += inst_gam
                Memory.writeInstr(temp_pc, (1 if int(command[1]) >= 0 else -1)*(int(command[1]) if int(command[1]) > 0 else (-int(command[1]))//int(pow(2, 8))))
                temp_pc += inst_gam
                Memory.writeInstr(temp_pc, int(command[1])%int(pow(2, 8)) if int(command[1]) >= 0 else (int(command[1])%int(pow(2, 8)) - int(pow(2, 8))))
                temp_pc += inst_gam
            elif command[0] == "IFEQ":
                Memory.writeInstr(temp_pc, 153)
                temp_pc += inst_gam
                Memory.writeInstr(temp_pc, (1 if int(command[1]) >= 0 else -1) * (
                int(command[1]) if int(command[1]) > 0 else (-int(command[1])) // int(pow(2, 8))))
                temp_pc += inst_gam
                Memory.writeInstr(temp_pc, int(command[1]) % int(pow(2, 8)) if int(command[1]) >= 0 else (
                int(command[1]) % int(pow(2, 8)) - int(pow(2, 8))))
                temp_pc += inst_gam
            elif command[0] == "IFLT":
                Memory.writeInstr(temp_pc, 155)
                temp_pc += inst_gam
                Memory.writeInstr(temp_pc, (1 if int(command[1]) > 0 else -1) * (
                int(command[1]) if int(command[1]) >= 0 else (-int(command[1])) // int(pow(2, 8))))
                temp_pc += inst_gam
                Memory.writeInstr(temp_pc, int(command[1]) % int(pow(2, 8)) if int(command[1]) >= 0 else (
                int(command[1]) % int(pow(2, 8)) - int(pow(2, 8))))
                temp_pc += inst_gam
            elif command[0] == "IF_ICMPEQ":
                Memory.writeInstr(temp_pc, 159)
                temp_pc += inst_gam
                Memory.writeInstr(temp_pc, (1 if int(command[1]) > 0 else -1) * (
                int(command[1]) if int(command[1]) >= 0 else (-int(command[1])) // int(pow(2, 8))))
                temp_pc += inst_gam
                Memory.writeInstr(temp_pc, int(command[1]) % int(pow(2, 8)) if int(command[1]) >= 0 else (
                int(command[1]) % int(pow(2, 8)) - int(pow(2, 8))))
                temp_pc += inst_gam
            elif command[0] == "ILOAD":
                Memory.writeInstr(temp_pc, 21)
                temp_pc += inst_gam
                Memory.writeInstr(temp_pc, int(command[1]))
                temp_pc += inst_gam
            elif command[0] == "ISTORE":
                Memory.writeInstr(temp_pc, 52)
                temp_pc += inst_gam
                Memory.writeInstr(temp_pc, int(command[1]))
                temp_pc += inst_gam
            elif command[0] == "HEX":
                Memory.writeData(temp_pc, int(command[1], 16))
                temp_pc += dat_gam
            elif command[0] == "DEC":
                Memory.writeData(temp_pc, int(command[1]))
                temp_pc += dat_gam
            else:
                pass

        elif len(command) == 3:
            if command[0] == "IINC":
                Memory.writeInstr(temp_pc, 132)
                temp_pc += inst_gam
                Memory.writeInstr(temp_pc, int(command[1]))
                temp_pc += inst_gam
                Memory.writeInstr(temp_pc, int(command[2]))
                temp_pc += inst_gam
            else:
                pass
        line = file.readline()

temp_registers = copy.deepcopy(Registers)
temp_flops = copy.deepcopy(Flip_flaps)
idle_time = 0
def next_inst():
    global total_delay, temp_registers, temp_flops, idle_time
    instruction, delay = Memory.readInstr(getRegister(Registers, "PC").amount)
    # total_delay += delay
    if instruction == 1000:
        instruction = Instruction(0, "HLT", 0, 0, Registers, Signals, Memory, Flip_flaps)
        showEVERYTHING(temp_registers, temp_flops, instruction)
        sim.FINISH = True
        return
    elif instruction == 0:
        instruction = Instruction(0, "NOP", 0, 0, Registers, Signals, Memory, Flip_flaps)
    elif instruction == 96:
        instruction = Instruction(0, "IADD", 96, 0, Registers, Signals, Memory, Flip_flaps)
    elif instruction == 100:
        instruction = Instruction(0, "ISUB", 100, 0, Registers, Signals, Memory, Flip_flaps)
    elif instruction == 16:
        instruction = Instruction(0, "BIPUSH", 16, 0, Registers, Signals, Memory, Flip_flaps)
    elif instruction == 167:
        instruction = Instruction(0, "GOTO", 167, 0, Registers, Signals, Memory, Flip_flaps)
    elif instruction == 153:
        instruction = Instruction(0, "IFEQ", 153, 0, Registers, Signals, Memory, Flip_flaps)
    elif instruction == 155:
        instruction = Instruction(0, "IFLT", 155, 0, Registers, Signals, Memory, Flip_flaps)
    elif instruction == 159:
        instruction = Instruction(0, "IF_ICMPEQ", 159, 0, Registers, Signals, Memory, Flip_flaps)
    elif instruction == 21:
        instruction = Instruction(0, "ILOAD", 21, 0, Registers, Signals, Memory, Flip_flaps)
    elif instruction == 52:
        instruction = Instruction(0, "ISTORE", 52, 0, Registers, Signals, Memory, Flip_flaps)
    elif instruction == 132:
        instruction = Instruction(0, "IINC", 132, 0, Registers, Signals, Memory, Flip_flaps)
    done = False
    while not done:
        tmp_delay, done = instruction.stepForward()
        # idle_time += tmp_delay -1
        for i in range(tmp_delay):
            total_delay += 1
            showEVERYTHING(temp_registers, temp_flops,instruction)
        temp_registers = copy.deepcopy(Registers)
        temp_flops = copy.deepcopy(Flip_flaps)

def showEVERYTHING(copiesR, copiesF, instruction):
    global Registers, Flip_flaps
    reg_texts = []
    for i in range(len(Registers)):
        r = copiesR[i]
        t = Registers[i]
        text = r.name + " : " + str(r.amount) + "\n"
        for s in t.signals:
            text += "    " + s.operation + " : " + str(s.amount) + "\n"
        reg_texts.append(text)
    # for r in Registers:

    for i in range(len(Flip_flaps)):
        r = copiesF[i]
        t = Flip_flaps[i]
    # for r in Flip_flaps:
        text = r.name + " : " + str(r.amount) + "\n"
        for s in t.signals:
            text += "   " + s.operation + " : " + str(s.amount) + "\n"
        reg_texts.append(text)

    if type(instruction) == Instruction:
        reg_texts.append("BUS Signals : " + instruction.BUSSignals)
        reg_texts.append("ALU Signals : " + instruction.ALUSignals)
    else:
        temp_instruction = Instruction(5, 5, 5, 5, 5, 5, 5, 5)
        reg_texts.append("BUS Signals : " + temp_instruction.BUSSignals)
        reg_texts.append("ALU Signals : " + temp_instruction.ALUSignals)

    text = ""
    for s in Signals:
        if s.moduleName == "Memory":
            text += s.operation + " : " + str(s.amount) + "\n"
    reg_texts.append(text)

    sim.inst_name = (instruction.name)
    sim.reg_texts.append(reg_texts)
