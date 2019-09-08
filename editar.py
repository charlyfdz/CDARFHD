from tkinter import *
import json 
from listasydiccionarios import *
from facetrack_new import *

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

def openWindow():
    ventana_editar()

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
nombre=Label(miframe,text="Nombre:",fg="black").grid(row=1,column=0,pady=4)
inputNombre = Entry(miframe, textvariable=minombre).grid(row=1,column=1,pady=4)

nivel=Label(miframe,text="Nivel de acceso:",fg="black").grid(row=2,column=0,pady=4)
inputNivel = Entry(miframe,textvariable=minivel).grid(row=2,column=1,pady=4)

foto=Label(miframe,text="Nueva fotografía:",fg="black").grid(row=3,column=0,pady=4)
inputFoto = Entry(miframe,textvariable=miFoto).grid(row=3,column=1,pady=4)

huella=Label(miframe,text="Nueva Huella digital:",fg="black").grid(row=4,column=0,pady=4)
inputHuella = Entry(miframe,textvariable=miHuella).grid(row=4,column=1,pady=4)

listbox = Listbox(miframe)
listbox.grid(row=0,column=6)
cargar =Button(miframe,text="cargar datos",  command = lambda listbox=listbox: buscar(listbox.get(ANCHOR),"cargar")).grid(row=1,column=6,pady=4)

for item in range(len(datos)):
    dato=datos[item]["nombre"]
    listbox.insert(END, dato)

iniciar=Button(miframe,text="Iniciar Camaras",highlightbackground='#3E4149',command=iniciarTracking).grid(row=0,column=1)


nuevo = Button(miframe,text="Nuevo usuario", command=crear_nuevo_usuario).grid(row=5,column=4,pady=4)
borrar = Button(miframe,text="Eliminar usuario", command=lambda: borra_ui(listbox.get(ANCHOR))).grid(row=5, column=5,pady=4)
actualizar =Button(miframe,text="actualizar", command=lambda: buscar(listbox.get(ANCHOR),"actualizar")).grid(row=5,column=6,pady=4)

tomarfoto=Button(miframe,text="tomar foto", command=lambda: tomar_imagen(minombre.get())).grid(row=2,column=2,pady=4)
verfoto=Button(miframe,text="ver foto", command=lambda: ver_foto(miFoto.get())).grid(row=2,column=3,pady=4)
tomarhuella=Button(miframe,text="tomar huella", command=lambda: tomar_huella(listbox.get(ANCHOR))).grid(row=3,column=2,pady=4)

regresar=Button(miframe,text="Cerrar", command=miframe.quit).grid(row=6,column=5,pady=4)
#todos=Button(miframe,text="todos los usuarios", command=todousuarios).grid(row=5,column=0,pady=4)
root.mainloop()