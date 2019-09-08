
import serial.tools.list_ports
from tkinter import *
import json 
from listasydiccionarios import *
from facetrack_new import *
from PIL import Image

puerto = ""
def conectar(x):
    puerto=x
    print(puerto)

####################### configuracion ventana
width=500
height=300

root=Tk()
root.title("Editar")
root.iconbitmap("assets/logo.ico")
root.resizable(0,0)
miframe=Frame(root,width=width,height=height)
miframe.grid(row=1,column=1,padx=10,pady=10,columnspan=6)
miframe.pack()

listboxport = Listbox(miframe)
listbox.grid(row=0,column=6)
buscar =Button(miframe,text="cargar puertos",  command = lambda listbox=listbox: conectar(listbox.get(ANCHOR))).grid(row=1,column=6,pady=4)

plist = list(serial.tools.list_ports.comports())
for item in range(len(plist)):
    plis=plist[item][0]
    listbox.insert(END, plis)

root.mainloop()
