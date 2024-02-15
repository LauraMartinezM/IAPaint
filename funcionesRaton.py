import pyautogui
import mediapipe as mp
import cv2
import pygame
import numpy as np
import time

def detectarRostroVideo(frame):
    pyautogui.FAILSAFE = False #Para que no salte una excepción si el raton se mueve muy brusco de la nada 
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True) # Se crea la maya facial
    screen_w, screen_h = pyautogui.size() # Se recogen las dimensiones del monitor
    #Dimensiones del cuadro de efecto del raton (para evitar problemas de cuello)
    cuadro_W = 200
    cuadro_h = 100

    #Se aplica la maya al los frames de la camara
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    ouput = face_mesh.process(rgb_frame)
    landmarks_points = ouput.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape # Se recogen las dimensiones de los frames
    
    #Si hay una cara reconocida
    if landmarks_points:
        landmarks = landmarks_points[0].landmark

        # seguir la nariz
        for landmark in landmarks[1:2]: #para la posicion de la nairz
            # Recoger posición
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x,y), 3, (0,255,0)) #Dibujar un circulo en la punta de la nariz

            #Ajustar coordenadas del recuadro en comparación con el monitor
            dimension_x = np.interp(x, (cuadro_W, frame_w-cuadro_W), (0,screen_w))
            dimension_y = np.interp(y, (cuadro_h, frame_h-cuadro_h), (0,screen_h))

            
            cv2.rectangle(frame, (cuadro_W,cuadro_h),(frame_w - cuadro_W, frame_h-cuadro_h), (255,0,0), 1)# Dibujar rectangulo que deímita el movimiento del raton

            pyautogui.moveTo(dimension_x,dimension_y) # mover ratón en la pantalla respectivamente a la nariz en el recuadro

        #hacer clic
        #Se guardan las posiciones de la parte superior del parpado e inferior de los dos ojos   
        otroOjo = [landmarks[145], landmarks[159]]
        otroOjo_2 = [landmarks[374], landmarks[386]]
        
        for landmark, landmark_2 in otroOjo, otroOjo_2: # por cada ojo 
            pygame.init() # se inicia el espacio de la musica

            # se seleccionan las coordenadas (dos por ojo arriba del parpado y debajo) y se dibuja un circulo
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x,y), 3, (0,255,255))

            x = int(landmark_2.x * frame_w)
            y = int(landmark_2.y * frame_h)
            cv2.circle(frame, (x,y), 3, (0,255,255))

            # Si ambos ojos estan cerrados se hace un clic y se reporduce un sonido de clic
            if (otroOjo[0].y - otroOjo[1].y) < 0.02 and (otroOjo_2[0].y - otroOjo_2[1].y) < 0.02:
                pygame.mixer.music.load("resources/clic.mp3")
                pygame.mixer.music.play()
                pyautogui.click()
                time.sleep(1)
            elif (otroOjo[0].y - otroOjo[1].y) < 0.02 and not pyautogui.mouseDown(): # si solo cierra el ojo derecho (cerrar y abrir) se mantienen pulsado el boton del clic y se reporduce un sonido de clic
                print("cerrado")
                pyautogui.mouseDown()
                pygame.mixer.music.load("resources/clic.mp3")
                pygame.mixer.music.play()
                time.sleep(1)
            elif (otroOjo_2[0].y - otroOjo_2[1].y) < 0.02: # si solo cierra el ojo izquierdo (cerrar y abrir) se levanta el boton del clic y se reporduce un sonido de clic
                print("cerrado ojo dos")
                pyautogui.mouseUp()
                pygame.mixer.music.load("resources/clic.mp3")
                pygame.mixer.music.play()
                time.sleep(1)

    return frame # Retorna el frame con las indicaciones (circulos y rectangulo)