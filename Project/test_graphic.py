import tkinter as tk
from PIL import Image, ImageTk
import cpu, sys
sys.setrecursionlimit(1000000)

file = None
pc, lv, cpp, sp, write, arch, evict, size, file = 0, 0, 0, 0, 0, 0, 0, 0, 0
reg_texts =[]
sim = 5
# temp = cpu.Registers[0]
class Settings:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(self.root)
        self.window.title("SIMULATOR Settings")
        self.window.geometry("1280x760")

        self.backgroundColor = '#000033'
        self.window.configure(background=self.backgroundColor)
        self.window.resizable(0,0)

        self.label = tk.Label(self.window, text='Welcome to CPU Simulator')
        self.label.place(x = 640, y = 100, anchor='center')

        self.callToAction = tk.Label(self.window, text='Please configure the required settings for your CPU.')
        self.callToAction.place(x = 640, y = 200, anchor='center')

        self.Initalize_label = tk.Label(self.window, text='Enter initial values for required regs.', background='light blue')
        self.Initalize_label.place(x = 60, y = 400, anchor='nw')
        self.PC_label = tk.Label(self.window, text='PC')
        self.PC_label = tk.Label(self.window, text='PC')
        self.PC_field = tk.Entry(self.window, )
        self.PC_label.place(x = 100, y = 500, anchor='center')
        self.PC_field.place(x = 180, y = 500, anchor='center')

        self.LV_label = tk.Label(self.window, text='LV')
        self.LV_field = tk.Entry(self.window, )
        self.LV_label.place(x = 100, y = 550, anchor='center')
        self.LV_field.place(x = 180, y = 550, anchor='center')

        self.CPP_label = tk.Label(self.window, text='CPP')
        self.CPP_field = tk.Entry(self.window, )
        self.CPP_label.place(x = 100, y = 600, anchor='center')
        self.CPP_field.place(x = 180, y = 600, anchor='center')

        self.SP_label = tk.Label(self.window, text='SP')
        self.SP_field = tk.Entry(self.window, )
        self.SP_label.place(x = 100, y = 650, anchor='center')
        self.SP_field.place(x = 180, y = 650, anchor='center')

        self.cache_set = tk.Label(self.window, text='Enter proper cache settings.', background='light blue')
        self.cache_set.place(x=400, y=400, anchor='nw')
        self.cache_arch = tk.IntVar()
        self.Direct_Mapped = tk.Radiobutton(self.window, text="Direct Mapped", variable=self.cache_arch, value=0)
        self.Two_Way = tk.Radiobutton(self.window, text="Two Way", variable=self.cache_arch, value=1)
        self.Four_Way = tk.Radiobutton(self.window, text="Four Way", variable=self.cache_arch, value=2)
        self.Direct_Mapped.place(x = 350, y = 500, anchor='nw')
        self.Two_Way.place(x = 350, y = 530, anchor='nw')
        self.Four_Way.place(x = 350, y = 560, anchor='nw')

        self.Cache_Size_label = tk.Label(self.window, text='Cache Size')
        self.Cache_Size_field = tk.Entry(self.window, )
        self.Cache_Size_label.place(x = 550, y = 510, anchor='center')
        self.Cache_Size_field.place(x = 650, y = 510, anchor='center')

        self.write_policy = tk.IntVar()
        self.Write_Back = tk.Radiobutton(self.window, text="Write Back", variable=self.write_policy, value=0)
        self.Write_Through = tk.Radiobutton(self.window, text="Write Through", variable=self.write_policy, value=1)
        self.Write_Back.place(x = 350, y = 600, anchor='nw')
        self.Write_Through.place(x = 350, y = 630, anchor='nw')

        self.eviction_type = tk.IntVar()
        self.LRU = tk.Radiobutton(self.window, text="LRU", variable=self.eviction_type, value=0)
        self.MRU = tk.Radiobutton(self.window, text="MRU", variable=self.eviction_type, value=1)
        self.Random = tk.Radiobutton(self.window, text="Random", variable=self.eviction_type, value=3)
        self.FIFO = tk.Radiobutton(self.window, text="FIFO", variable=self.eviction_type, value=2)
        self.BIP = tk.Radiobutton(self.window, text="BIP", variable=self.eviction_type, value=4)
        self.LRU.place(x = 550, y = 550, anchor='nw')
        self.MRU.place(x = 550, y = 580, anchor='nw')
        self.Random.place(x = 550, y = 610, anchor='nw')
        self.FIFO.place(x = 550, y = 640, anchor='nw')
        self.BIP.place(x = 550, y = 670, anchor='nw')

        self.code_label = tk.Label(self.window, text='Provide your assembley Code.',background='light blue')
        self.code_label.place(x=860, y=400, anchor='nw')
        self.browse = tk.Button(self.window, text='Browse Your Assembley Code', command=self.receiveFile, activebackground='yellow')
        self.browse.place(x=850, y=500)
        self.file_label = tk.Label(self.window)
        self.file_label.place(x=850, y=530)

        self.done = tk.Button(self.window, text='DONE !', command=self.set_settings_and_leave, activebackground='yellow', background='turquoise')
        self.done.place(x=1200, y=700, anchor='nw')


    def receiveFile(self):
        global file
        from tkinter.filedialog import askopenfile
        file = askopenfile()
        self.file_label.config(text=file.name, background='yellow')


    def set_settings_and_leave(self):
        global reg_texts, sim, file
        pc = int(self.PC_field.get())
        cpp = int(self.CPP_field.get())
        lv = int(self.LV_field.get())
        sp = int(self.SP_field.get())

        evict = int(self.eviction_type.get())
        write = int(self.write_policy.get())
        arch = int(self.cache_arch.get())

        size = int(self.Cache_Size_field.get())

        cpu.getRegister(cpu.Registers, "PC").amount, cpu.getRegister(cpu.Registers, "SP").amount, cpu.getRegister(cpu.Registers, "LV").amount, \
        cpu.getRegister(cpu.Registers, "CPP").amount = pc, sp, lv, cpp

        cpu.Cache.memorySize, cpu.Cache.cacheSize = len(cpu.Memory.array), size
        cpu.cacheArch, cpu.writeType, cpu.evictType = arch, write, evict

        cpu.cache = cpu.Cache.Cache(cpu.cacheArch, cpu.writeType, cpu.evictType)
        cpu.Cache.memory = cpu.Memory.array

        cpu.file = file

        sim = Simulator(self.root, reg_texts)
        cpu.sim = sim

        cpu.do()
        self.window.destroy()

        return pc, cpp, lv, sp, evict, write, arch, size

class Simulator():
    def __init__(self, root, reg_texts):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("SIMULATOR SHOW")
        self.window.geometry("1280x760")
        self.FINISH = False
        self.reg_texts = []

        self.backgroundColor = '#000033'
        self.window.configure(background=self.backgroundColor)
        self.window.resizable(0, 0)

        self.counter = -5

        self.x = [5, 205, 405, 605, 805, 1005, 5, 205, 405, 605, 805, 1005, 5, 205, 405, 605, 805, 1005, 5, 205, 405, 605, 805, 1005]
        self.y = [5, 5, 5, 5, 5, 5, 205, 205, 205, 205, 205, 205, 405, 405, 405, 405, 405, 405, 605, 605, 605, 605, 605, 605]

        self.update_simulator()

    # def giveImg(self, input_window):
    #     img = Image.open("./ic.jpg")
    #     img = ImageTk.PhotoImage(img)
    #     return tk.Label(input_window, image=img)

    def update_simulator(self):
        # cpu.next_inst()
        self.window.destroy()
        self.window = tk.Toplevel(self.root)
        self.window.title("SIMULATOR SHOW")
        self.window.geometry("1280x760")

        self.backgroundColor = '#000033'
        self.window.configure(background=self.backgroundColor)
        self.window.resizable(0, 0)

        self.next = tk.Button(self.window, text='Start/Next', command=self.nextclk, background='turquoise')
        self.next.place(x=1200, y=700, anchor='nw')

        self.MemShow = tk.Button(self.window, text='Show Four Bytes', command=self.showMem, background='turquoise')
        self.MemShow.place(x=1000, y=700, anchor='nw')

        self.MemShow_one = tk.Button(self.window, text='Show One Byte', command=self.showMem_one, background='turquoise')
        self.MemShow_one.place(x=900, y=700, anchor='nw')

        self.MemShowField = tk.Entry(self.window, text="Enter memory field you want to check.", background='light blue')
        self.MemShowField.place(x=750, y=700, anchor='nw')


        utilization_label = tk.Label(self.window, text="Utilization Rate :", background='beige')
        utilization_label.place(x=900, y=550)

        inst_name_label = tk.Label(self.window, text="Instruction :", background='beige')
        inst_name_label.place(x=1050, y=550)

        Label = tk.Label(self.window, text="Hit Rate :", background='beige')
        Label.place(x=900, y=600)

        throughput_label = tk.Label(self.window, text="Throughput :", background='beige')
        throughput_label.place(x=900, y=650)

        self.mem_one_label = tk.Label(self.window)
        self.hitRate = tk.Label(self.window)
        self.throughput = tk.Label(self.window)
        self.utilization = tk.Label(self.window)
        self.inst_name_Label = tk.Label(self.window)

        self.numOfInstructions = 0
        self.numOfClks = 0
        self.task = 0
        self.inst_name = ""

    def showMem(self):
        address = int(self.MemShowField.get())
        data = cpu.Memory.readData(address)[0]
        # print(data)
        # print(cpu.Memory.array[address])
        self.mem_one_label.destroy()
        self.mem_one_label = tk.Label(self.window, text=str(data))
        self.mem_one_label.place(x=1000, y=725)

    def showMem_one(self):
        address = int(self.MemShowField.get())
        data = cpu.Memory.array[address]
        # print(data)
        # print(cpu.Memory.array[address])
        self.mem_one_label.destroy()
        self.mem_one_label = tk.Label(self.window, text=str(data))
        self.mem_one_label.place(x=900, y=725)

    def nextclk(self):
        self.numOfClks += 1
        if self.FINISH:
            sub_window = tk.Toplevel(self.window)
            sub_window.title("PROCESSOR STOPPED BY HLT INSTRUCTION")
            sub_window.geometry("600x200")
            sub_window.configure(background="red")
            message = tk.Label(sub_window, text= "INSTRUCTION \"HLT\" HAS BEEN FETCHED.")
            message.place(x=300 , y=100 ,anchor='center')
            return
        if self.counter >= len(self.reg_texts) or self.counter < 0:
            self.counter = 0
            self.reg_texts = []
            self.numOfInstructions += 1
            cpu.next_inst()
        # print((len(self.reg_texts[self.counter])))
        for i in range(len(self.reg_texts[self.counter])):
            Label = tk.Label(self.window, text=self.reg_texts[self.counter][i], background='white' if i < 14 else 'silver')
            Label.place(x=self.x[i], y=self.y[i])

        if self.counter == len(self.reg_texts) - 1:
            self.task += 1

        self.hitRate.destroy()
        self.hitRate = tk.Label(self.window, text=str(round(cpu.Cache.hits/(cpu.Cache.hits+cpu.Cache.misses), 2)), background='beige')
        self.hitRate.place(x=1000, y=600)

        self.throughput.destroy()
        self.throughput = tk.Label(self.window, text=str(round(self.numOfInstructions / self.numOfClks, 2)) + "f", background='beige')
        self.throughput.place(x=1000, y=650)

        self.utilization.destroy()
        self.utilization = tk.Label(self.window, text=str(round((self.numOfClks-self.task) / self.numOfClks, 2)), background='beige')
        self.utilization.place(x=1000, y=550)

        self.inst_name_Label.destroy()
        self.inst_name_Label = tk.Label(self.window, text=self.inst_name, background='beige')
        self.inst_name_Label.place(x=1150, y=550)

        self.counter += 1
        self.window.update()

def start():
    root = tk.Tk()
    Settings(root)
    root.withdraw()
    root.mainloop()
    return

start()