from tkinter import *
import json 
from listasydiccionarios import *
from PIL import Image
import serial.tools.list_ports
import face_recognition
import cv2
import numpy as np
import os
import serial,time


def comu(x):
    port = x
    baud=9600
    arduino = serial.Serial(port=port, baudrate=baud, timeout=.1)
    time.sleep(1)
    iniciarTracking(arduino)

######################################################################################
######################################################################################
######################comunicacion serial y reconocimiento dacial#####################
######################################################################################
######################################################################################
#############################comunicacion serial



def iniciaCom(v,arduino):
    if v==1:
        leer(arduino)
    elif v==0:
        cerrar(arduino)

def leerSerial(arduino):
    data = arduino.readline()
    arr = str(data)
    if data:
        print (arr)

def abrir(arduino):
    arduino.write(b"1")
    print("abierto")
    leerSerial(arduino)

def cerrar(arduino):
    arduino.write(b"0")
    print("cerrado")
    leerSerial(arduino)
###################################################################
##################reconocimiento facial #############################

def usuario_bienvenido(name,arduino):
    if name=="Unknown":
        cerrar(arduino)
        #print("no registrado")
    else:
        abrir(arduino)
        #print("Bienvenido: "+name)

def iniciarTracking(arduino):
    
    datos=leer()
    matrices=[]
    encodes=[]

    known_face_encodings = []
    known_face_names = []
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    for i in range(len(datos)):
        dato=datos[i]["foto"]
        matrices.append(face_recognition.load_image_file(dato))
        matriz=matrices[i]
        known_face_encodings.append(face_recognition.face_encodings(matriz)[0])

    for i in range(len(datos)):
        known_face_names.append(datos[i]["nombre"])

    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []

            if face_encodings ==[]:
                cerrar(arduino)


            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                
                name = "Unknown"
                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]
                
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    usuario_bienvenido(name,arduino)
                
                face_names.append(name)

        process_this_frame = not process_this_frame

        
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            arduino.close()
            break
    
    video_capture.release()
    cv2.destroyAllWindows()


######################################################################################
######################################################################################
#######################end reconocimiento y serial ###################################
######################################################################################
######################################################################################


####################### configuracion ventana principal
width=500
height=300

root=Tk()
root.title("Editar")
root.iconbitmap("assets/logo.ico")
root.resizable(0,0)
miframe=Frame(root,width=width,height=height)
miframe.grid(row=1,column=1,padx=10,pady=10,columnspan=6)
miframe.pack()
###########################################################

############  variables de widgets
minombre=StringVar()
minivel=StringVar()
miFoto=StringVar()
miHuella=StringVar()
idlistbox=StringVar()
id=0

###########################################################

###########################33 funciones de accion


def conectar(x):
    port=x

def actualizar_valores_usuario(valorid):
    nombre = minombre.get()
    nivel = minivel.get()
    foto = miFoto.get()
    huella = miHuella.get()
    datos[valorid]["nombre"]=nombre
    datos[valorid]["nivel"]=nivel
    datos[valorid]["foto"]=foto
    datos[valorid]["huella"]=huella
    escribir(datos)
    cargardatos(valorid)
    refreshListbox()


def crear_nuevo_usuario():
    nombre = minombre.get()
    nivel = minivel.get()
    foto = miFoto.get()
    huella = miHuella.get()
    datos=leer()
    if nombre!="" and nivel!="" and foto!="":
        id=0
        for i in datos:
            if i.get("nombre")==nombre.capitalize():
                print("usuario existente")
                return 0
        datos.append({"nombre":nombre,"nivel":nivel,"foto":foto,"huella":huella})
        escribir(datos)
        refreshListbox()

    else:
        print("valores incorrecto")
    

def cargardatos(id):
    datos=leer()
    minombre.set(datos[id]["nombre"])
    minivel.set(datos[id]["nivel"])
    miFoto.set(datos[id]["foto"])
    miHuella.set(datos[id]["huella"])

def refreshListbox():
    datos=leer()
    for item in range(len(datos)+1):
        listbox.delete(0,item)
    for newitem in range(len(datos)):
        dato=datos[newitem]["nombre"]
        listbox.insert(END, dato)

def borra_ui(nombre):
    borrar_usuario(nombre)
    refreshListbox()


def buscar(nombre,tipo):
    id=0
    datos=leer()
    for i in datos:
        if i.get("nombre")==nombre:
            break
        else:
            id=id+1
    if tipo=="actualizar":
        actualizar_valores_usuario(id)
    elif tipo=="cargar": 
        cargardatos(id)

def nothing(x):
    pass

def ver_foto(nombre):
    img = cv2.imread(nombre)
    px = img[100,100]
    blue = img[100,100,0]
    img[100,100]=[255,255,255]
    img.itemset((10,10,2),100)
    cv2.imshow(nombre,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def tomar_imagen(nombre):
    if nombre=="":
        return 0
    print(nombre)
    nombre_foto=""
    cap = cv2.VideoCapture(0)
    cap.set(3,640) #width=640
    cap.set(4,480) 
    while(True):
        ret, frame = cap.read()
        cv2.imshow('web cam',frame)
        if cv2.waitKey(1) & 0xFF == ord('p'):
            nombre_foto='fotos/'+nombre.lower().replace(" ","_")+".jpg"
            cv2.imwrite(nombre_foto, frame)
            cap.release()
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break

    cv2.imshow(nombre_foto,frame)
    k = cv2.waitKey(0) & 0xFF
    if k == ord('s'):
        miFoto.set(nombre_foto)
        cv2.destroyAllWindows()
    return nombre_foto

def tomar_huella(nombre):
    if nombre=="":
        return 0
    return 0
#######################################################

################## datos de usuarios
datos=leer()

############################################################

################################### widgets
########################columna 1
img = PhotoImage(file='assets/logo.gif')
logoimg=Label(miframe,image=img).grid(row=0,column=0)
logo=Label(miframe,text="UNIVERSIDAD AUTONOMA DE BAJACALIFORNIA SUR").grid(row=1,column=0)

nombre=Label(miframe,text="Nombre:",fg="black").grid(row=2,column=0,pady=4)
nivel=Label(miframe,text="Nivel de acceso:",fg="black").grid(row=3,column=0,pady=4)
foto=Label(miframe,text="Fotografía:",fg="black").grid(row=4,column=0,pady=4)
huella=Label(miframe,text="Huella digital:",fg="black").grid(row=5,column=0,pady=4)

####################################################

#######################columna 2
listbox = Listbox(miframe)
listbox.grid(row=0,column=1)
cargar =Button(miframe,text="cargar datos",  command = lambda listbox=listbox: buscar(listbox.get(ANCHOR),"cargar")).grid(row=1,column=1,pady=4)

for item in range(len(datos)):
    dato=datos[item]["nombre"]
    listbox.insert(END, dato)


inputNombre = Entry(miframe, textvariable=minombre).grid(row=2,column=1,pady=4)
inputNivel = Entry(miframe,textvariable=minivel).grid(row=3,column=1,pady=4)
inputFoto = Entry(miframe,textvariable=miFoto).grid(row=4,column=1,pady=4)
inputHuella = Entry(miframe,textvariable=miHuella).grid(row=5,column=1,pady=4)



#########################################################

######################columna 3

listboxport = Listbox(miframe)
listboxport.grid(row=0,column=2)
plist = list(serial.tools.list_ports.comports())
for item in range(len(plist)):
    plis=plist[item][0]
    listboxport.insert(END, plis)

nuevo = Button(miframe,text="Nuevo usuario", command=crear_nuevo_usuario).grid(row=7,column=2,pady=4)
tomarfoto=Button(miframe,text="tomar foto", command=lambda: tomar_imagen(minombre.get())).grid(row=4,column=2,pady=4)
tomarhuella=Button(miframe,text="tomar huella", command=lambda: tomar_huella(listbox.get(ANCHOR))).grid(row=5,column=2,pady=4)
borrar = Button(miframe,text="Eliminar usuario", command=lambda: borra_ui(listbox.get(ANCHOR))).grid(row=7, column=5,pady=4)



########################################################

#######################columna 4
iniciar=Button(miframe,text="Iniciar Camaras",highlightbackground='#3E4149',command=lambda: comu(listboxport.get(ANCHOR))).grid(row=0,column=3)

verfoto=Button(miframe,text="ver foto", command=lambda: ver_foto(miFoto.get())).grid(row=4,column=3,pady=4)
actualizar =Button(miframe,text="actualizar", command=lambda: buscar(listbox.get(ANCHOR),"actualizar")).grid(row=7,column=3,pady=4)

regresar=Button(miframe,text="Cerrar", command=miframe.quit).grid(row=8,column=3,pady=4)


#####################################################

root.mainloop()