import json
import numpy as np
import cv2

def escribir(lista):
    with open('data/lista.txt', 'w') as filehandle:
        for listitem in lista:
            filehandle.write('%s\n' % listitem)
        filehandle.close()

def leer():
    datos=[]
    datos_salida=[]
    with open('data/lista.txt', 'r') as filehandle:
        for line in filehandle:
            # remove linebreak which is the last character of the string
            currentdata = line[:-1]

            # add item to the list
            datos.append(currentdata)
        filehandle.close()

    for i in datos:
        s = i
        json_acceptable_string = s.replace("'", "\"")
        d = json.loads(json_acceptable_string)
        nombre=d["nombre"]
        nivel=d["nivel"]
        foto=d["foto"]
        huella=d["huella"]
        datos_salida.append({"nombre":nombre,"nivel":nivel,"foto":foto,"huella":huella})
        
    return datos_salida

def borrar_usuario(nombre):
    datos=leer()
    id=0
    for i in datos:
        if i.get("nombre")==nombre:
            del datos[id]
            escribir(datos)
        else:
            id=id+1


def todousuarios():
    datos=leer()
    print(datos)

# lista=[{
#     "nombre":'Carlos',
#     "nivel":5,
#     "foto":"fotos/carlos.jpg",
#     "huella":1
#     },
#     {
#     "nombre":'Jelena',
#     "nivel":4,
#     "foto":"fotos/jelena.jpg",
#     "huella":2
#     },
#     {
#     "nombre":'Julia',
#     "nivel":5,
#     "foto":"fotos/julia.jpg",
#     "huella":3
#     },
#     {
#     "nombre":'Vicktoria',
#     "nivel":5,
#     "foto":"fotos/viktoria.jpg",
#     "huella":3
#     }
#     ]


