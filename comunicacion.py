import serial, time
from tkinter import *

port="/dev/cu.usbmodem14201"
baud=9600
correcto = False
arduino = serial.Serial(port=port, baudrate=baud, timeout=.1)
time.sleep(1)

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

encender=StringVar()
apagar=StringVar()
id=0
###########################################################

def leerSerial():
    data = arduino.readline()
    arr = str(data)
    if data:
        print (arr)

def abrir():
    arduino.write(b"1")
    leerSerial()

def cerrar():
    arduino.write(b"0")
    leerSerial()


nuevo = Button(miframe,text="ecender", command=abrir).grid(row=2,column=1,pady=4)
borrar = Button(miframe,text="apagar", command=cerrar).grid(row=3, column=1,pady=4)



root.mainloop()