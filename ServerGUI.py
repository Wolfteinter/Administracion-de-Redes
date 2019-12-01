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
                        font="Arial",text="Nombre: "+ i.getData()[0] +"\n SO: "+ i.getData()[1],command=lambda: self.showInfoDis(i))
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

        btn1 = tk.Button(windowInfo,height=4,font=("Arial",15), width=100,text="Matriz(fuente - destino)")
        btn1.pack()

        btn2 = tk.Button(windowInfo,height=4,font=("Arial",15), width=100,text="Histograma de tipo de paquetes")
        btn2.pack()

        btn3 = tk.Button(windowInfo,height=4,font=("Arial",15), width=100,text="Histograma de tamaño de paquetes")
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

root = tk.Tk()
my_gui = ServerGUI(root)
