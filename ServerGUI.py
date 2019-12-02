import tkinter as tk
from Server import Server
import socket, threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import time
import psutil
import numpy as np
from NTGraphGUI import NTGraphGUI
import os
#import pandas as pd
class VerticalScrolledFrame(tk.Frame):
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL,width=20)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.TRUE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set,height = 500)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)
        def _configure_interior(event):
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)
        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)
        interior.bind_all('<MouseWheel>', lambda event:     vscrollbar.yview("scroll",event.delta,"units"))

class ServerGUI(object):
    def __init__(self, master):
        self.master = master
        self.server = Server()
        ##Init of the master view
        self.master.title("Server GUI")
        self.master.configure(background="gray99")
        self.master.resizable(False,False)
        self.master.geometry("500x600")
        self.master.config(bg="#857074")
        #Header
        self.header = tk.Frame()
        self.header.pack(fill="y",pady=10)
        self.header.config(width="400",height="100",bg="#857074")
        self.title = tk.Label(self.header,text="Monitoreo de la red",font=("Arial",30),bg="#857074")
        self.title.pack()
        photo=tk.PhotoImage(file="Imagenes/histograma.png")
        self.info = tk.Button(self.header,image=photo,bg="#857074",bd=0,highlightthickness=0,command = self.showInfoSev)
        self.info.pack()
        #monitoring
        self.display = tk.Frame()
        self.display.pack(fill="x",pady=10,side=tk.LEFT,anchor=tk.N)
        self.display.config(bg="#454545",width="700",height="400")
        self.scframe = VerticalScrolledFrame(self.display)
        self.scframe.pack()
        threading.Thread(target=self.addDispositive).start()
        self.master.mainloop()

    def greet(self):
        self.server.getDispositives()[0].request_data()
    def addDispositive(self,*args):
        while(True):
            for widget in self.scframe.interior.winfo_children():
                widget.destroy()
            for i in self.server.getDispositives():
                if(i.isConn() == True):
                    btn = tk.Button(self.scframe.interior, height=6, width=100, relief=tk.FLAT,compound="left",
                        bg="#aebbb2",
                        font="Arial",text="Nombre: "+ i.getData()[0] +"\n SO: "+ i.getData()[1] +"\n IPv4: "+ i.getData()[2],command=lambda: self.showInfoDis(i))
                        #"Nombre: "+ i.getData()[0] +"\n SO: "+ i.getData()[1]+"\n Subred: "+ i.getData()[2]+"\n IP: "+ i.getData()[3]
                    btn.pack(padx=10, pady=5, side=tk.TOP)
                else:
                    self.server.getDispositives().remove(i)
            time.sleep(1)
    def showInfoSev(self):
        windowInfo = tk.Toplevel(self.master)
        windowInfo.title("Servidor")
        windowInfo.config(bg="#813042")
        windowInfo.geometry("380x310")
        windowInfo.resizable(False,False)

        btn1 = tk.Button(windowInfo,height=4,font=("Arial",15), width=100,text="Matriz(fuente - destino)", command = self.matrixSrcDestGUI)
        btn1.pack()

        btn2 = tk.Button(windowInfo,height=4,font=("Arial",15), width=100,text="Histograma de tipo de paquetes",command=self.histTypeGUI)
        btn2.pack()

        btn3 = tk.Button(windowInfo,height=4,font=("Arial",15), width=100,text="Histograma de tam de paquetes",command = self.lenHistGUI)
        btn3.pack()

    def showInfoDis(self,dispositive):
        windowInfo = tk.Toplevel(self.master)
        windowInfo.title("dispositivo : "+str(dispositive.getData()[0]))
        windowInfo.config(bg="#813042")
        windowInfo.geometry("380x300")
        windowInfo.resizable(False,False)

        btn1 = tk.Button(windowInfo,height=4,font=("Arial",15), width=100,text="Trafico de red",command=lambda: self.graphNetworkTraffic(dispositive))
        btn1.pack()

        btn2 = tk.Button(windowInfo,height=4,font=("Arial",15), width=100,text="Reiniciar computadora",command=lambda: self.reboot(dispositive))
        btn2.pack()

        btn3 = tk.Button(windowInfo,height=4,font=("Arial",15), width=100,text="Apagar computadora",command=lambda: self.powerOff(dispositive))
        btn3.pack()
    def graphNetworkTraffic(self,dispositive):
        graph = tk.Tk()
        my_gui = NTGraphGUI(graph,dispositive)
        graph.mainloop()
    def powerOff(self,dispositive):
        dispositive.powerOff()
    def reboot(self,dispositive):
        dispositive.reboot()
    def matrixSrcDestGUI(self):
        windowInfo = tk.Toplevel(self.master)
        windowInfo.title("Matriz(fuente - destino)")
        windowInfo.config(bg="#813042")
        windowInfo.resizable(False,False)
        label = tk.Label(windowInfo,text="Matriz(fuente - destino)",font=("Arial",20)).grid(column=0, row=0)
        btn1 = tk.Button(windowInfo,font=("Arial",15), width=20,text="Go!",command=self.matrixSrcDest).grid(column=0, row=1)
        self.figMatrix = plt.Figure()
        self.canvasMatrix = FigureCanvasTkAgg(self.figMatrix, master=windowInfo)
        self.canvasMatrix.get_tk_widget().grid(column=0,row=2)
    def matrixSrcDest(self):
        dic = { }
        for i in self.server.getDispositives():
            dic[i.getData()[2]] = { }
        # Write data
        dataFile = open("ips.txt", "w")
        dataFile.write(str(dic))
        dataFile.close()
        # Launch magic script
        sudoPass = ""
        command = "python matrixSrcDest.py"
        os.system("echo %s|sudo -S %s" % (sudoPass,command))
        # Recover data
        fileData = open("ips.txt","r")
        data = str(fileData.read())
            # Convertir el string a diccionario
        dic = eval(data)
        for fuente, destinos in dic.items():
            print("Fuente:", fuente)
            print("Destinos: ")
            for dest, val in destinos.items():
                print(str(dest) + " con: " + str(val) + " paquete(s)")
            print("-"*16)

        os.remove("ips.txt")

    def histTypeGUI(self):
        windowInfo = tk.Toplevel(self.master)
        windowInfo.title("Histograma tipo de paquetes")
        windowInfo.config(bg="#813042")
        windowInfo.resizable(False,False)
        label = tk.Label(windowInfo,text="Histograma tipo de paquetes",font=("Arial",20)).grid(column=0, row=0)
        btn1 = tk.Button(windowInfo,font=("Arial",15), width=20,text="Empezar",command=self.histType).grid(column=0, row=1)
        self.figHT = plt.Figure()
        self.canvasHT = FigureCanvasTkAgg(self.figHT, master=windowInfo)
        self.canvasHT.get_tk_widget().grid(column=0,row=2)
        self.axHT = self.figHT.add_subplot(111)
        #self.axHT.set_ylim([0,1000])
    def histType(self):
        sudoPass = "Fra9805Wolf"
        command = "python packHist.py"
        os.system("echo %s|sudo -S %s" % (sudoPass,command))
        fileData = open("data.txt","r")
        data = str(fileData.read())
        data = data.rstrip('\n')
        data = data.split("|")
        for i in range(len(data)):
            data[i] = data[i].replace("[",'')
            data[i] = data[i].replace("]",'')
        print(data[0])
        ids = list(map(int, filter(None, data[0].split(','))))
        count = list(map(int, filter(None, data[1].split(','))))
        labels = list(map(str, filter(None, data[2].split(','))))
        self.axHT.bar(ids,count,color='g')
        self.axHT.set_xticks(ids)
        self.axHT.set_xticklabels(labels)
        self.axHT.set_xlabel('Tipos')
        self.axHT.set_ylabel('Cantidad paquetes')
        self.figHT.canvas.draw()
        os.remove("data.txt")
    def lenHistGUI(self):
        windowInfo = tk.Toplevel(self.master)
        windowInfo.title("Histograma tamaño de paquetes")
        windowInfo.config(bg="#813042")
        windowInfo.resizable(False,False)
        label = tk.Label(windowInfo,text="Histograma tamaño de paquetes",font=("Arial",20)).grid(column=0, row=0)
        btn1 = tk.Button(windowInfo,font=("Arial",15), width=20,text="Empezar",command=self.lenHist).grid(column=0, row=1)
        self.figLT = plt.Figure()
        self.canvasLT = FigureCanvasTkAgg(self.figLT, master=windowInfo)
        self.canvasLT.get_tk_widget().grid(column=0,row=2)
        self.axLT = self.figLT.add_subplot(111)
    def lenHist(self):
        sudoPass = ""
        command = "python lenHist.py"
        os.system("echo %s|sudo -S %s" % (sudoPass,command))
        fileData = open("data2.txt","r")
        data = str(fileData.read())
        data = data.rstrip('\n')
        data = data.split("|")
        for i in range(len(data)):
            data[i] = data[i].replace("[",'')
            data[i] = data[i].replace("]",'')
        tams = list(map(int, filter(None, data[0].split(','))))
        count = list(map(int, filter(None, data[1].split(','))))
        datas = list(zip(tams,count))
        datas.sort(key=lambda tup: tup[1],reverse=True)
        datas = datas[0:10]
        datas = list(zip(*datas))
        tams = list(datas[0])
        count = list(datas[1])
        ids = list(range(len(tams)))
        print(tams)
        print(count)
        print(ids)
        self.axLT.bar(ids,count,color='g')
        self.axLT.set_xticks(ids)
        self.axLT.set_xticklabels(tams)
        self.axLT.set_xlabel('Tamaños en bytes')
        self.axLT.set_ylabel('Cantidad paquetes')
        self.figLT.canvas.draw()
        os.remove("data2.txt")

root = tk.Tk()
my_gui = ServerGUI(root)
