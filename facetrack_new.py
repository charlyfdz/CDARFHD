import face_recognition
import cv2
import numpy as np
import os
from listasydiccionarios import *
import serial
import time


port=''
baud=9600
correcto = False
arduino = serial.Serial(port=port, baudrate=baud, timeout=.1)
time.sleep(1)
if v==1:
    leer()
elif v==0:
    cerrar()

def leerSerial():
    data = arduino.readline()
    arr = str(data)
    if data:
        print (arr)

def abrir():
    arduino.write(b"1")
    print("abierto")
    leerSerial()
    arduino.close()

def cerrar():
    arduino.write(b"0")
    print("cerrado")
    leerSerial()
    arduino.close()

###########################################################################

def usuario_bienvenido(x,name):
    if name=="Unknown":
        cerrar()
        #print("no registrado")
    else:
        abrir(x,1)
        #print("Bienvenido: "+name)

def iniciarTracking(x):
    
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
                cerrar()


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
                    usuario_bienvenido(name)
                
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
            break

    video_capture.release()
    cv2.destroyAllWindows()


