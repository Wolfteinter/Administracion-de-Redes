from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
class NTGraphGUI(object):
    def __init__(self,master,dispositive):
        self.master = master
        self.master.title("Trafico de red : "+str(dispositive.getData()[0]))
        self.x = np.arange(0, 2*np.pi, 0.01)
        self.label = tk.Label(self.master,text="Trafico de red").grid(column=0, row=0)
        self.fig = plt.Figure()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().grid(column=0,row=1)
        self.ax = self.fig.add_subplot(111)
        self.line, = self.ax.plot(self.x, np.sin(self.x))
        self.ani = animation.FuncAnimation(self.fig, self.animate, np.arange(1, 200), interval=25, blit=False)
    def animate(self,i):
        self.line.set_ydata(np.sin(self.x+i/10.0))  # update the data
        return self.line,
