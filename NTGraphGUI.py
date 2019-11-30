from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
class NTGraphGUI(object):
    def __init__(self,master,dispositive):
        self.dispositive = dispositive
        self.master = master
        self.master.title("Trafico de red : "+str(dispositive.getData()[0]))
        self.label = tk.Label(self.master,text="Trafico de red").grid(column=0, row=0)
        self.fig = plt.Figure()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().grid(column=0,row=1)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim([-100,10000])
        self.ax.set_ylim([-100,10000])
        #grid()
        self.t = 0
        self.xdata, self.ydata = [], []
        self.line, = self.ax.plot([], [], marker='o', color='r')
        self.ani = animation.FuncAnimation(self.fig, self.run, self.data_gen, blit=True, interval=0.5,repeat=True)

    def data_gen(self):
        if self.t >= 10000:
            self.xdata.clear()
            self.ydata.clear()
            self.t = 0
        self.t += 100
        y0 = self.dispositive.getPackages()
        time.sleep(1)
        y1 = self.dispositive.getPackages()
        y0 = int(y1)-int(y0)
        yield self.t, y0
    def run(self,data):
        x0,y0 = data
        self.xdata.append(x0)
        self.ydata.append(y0)
        self.line.set_data(self.xdata, self.ydata)
        time.sleep(.1)
        return self.line,
