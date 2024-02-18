from tkinter import *
from tkinter import colorchooser, ttk, filedialog, PhotoImage

import cv2
import mediapipe as mp
from PIL import Image, ImageTk, ImageDraw

import pyautogui
from PIL import Image, ImageGrab, ImageTk

from funcionesRaton import detectarRostroVideo
from recogerDatos import guardarRespuestas

import tensorflow as tf
from keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt


class Pintura: 
    def __init__(self,master):
        self.master = master
        self.color_fg = 'Black'
        self.color_bg = 'white'
        
        self.old_x = None
        self.old_y = None

        self.pen_width = 5
        self.drawWidgets()

        self.c.bind('<Button-1>', self.start_paint)  # Vincula start_paint al evento de clic del ratón
        self.c.bind('<B1-Motion>', self.paint)  # Vincula paint al evento de movimiento del ratón
        self.c.bind('<ButtonRelease-1>', self.stop_paint)  # Vincula stop_paint al evento de liberación del botón del ratón


        # Inicializar la captura de la cámara
        self.cap = cv2.VideoCapture(0)
        _, self.frame = self.cap.read()

        self.camera_label = Label(self.master)
        self.camera_label.grid(row=1,column=1, padx=20)

        self.update_camera()
        self.dibujo = None
    
    def start_paint(self, e):
        self.old_x = e.x
        self.old_y = e.y

    
    def paint(self, e):
        
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, e.x, e.y, width=self.pen_width, fill=self.color_fg, capstyle='round', smooth=True)

        self.old_x = e.x
        self.old_y = e.y
        
    def dibujar_punto(self, event):
        x = event.x
        y = event.y
        self.c.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")

    def stop_paint(self, e):
        self.old_x = None
        self.old_y = None

    def changedW(self, width):
        self.pen_width = float(width)

    def clearcanvas(self):
        self.c.delete(ALL)
        self.image = Image.new('RGB', (500, 400), self.color_bg)
        self.draw = ImageDraw.Draw(self.image)

    def change_fg(self, color):
        if color == 0:
            self.color_fg = "#EF3737"
        
        if color == 1:
            self.color_fg = "#376AEF"
        
        if color == 2:
            self.color_fg = "#000000"
        

    def change_bg(self):
        self.color_bg = colorchooser.askcolor(color=self.color_bg)[1]
        self.c['bg'] = self.color_bg
    
    def save_image(self, file_path):
        print("Intentando guardar imagen", file_path+".png")
        #file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            # Obtener las dimensiones del canvas
            x0 = self.c.winfo_rootx()
            y0 = self.c.winfo_rooty()
            x1 = x0 + self.c.winfo_width()
            y1 = y0 + self.c.winfo_height()
            
            # Capturar el contenido del canvas como una imagen
            img = ImageGrab.grab(bbox=(x0, y0, x1, y1))
            try:
                # Guardar la imagen como un archivo PNG
                img.save((file_path+".jpg"))
                print("imagen guardada")
                return True
            except:
                return False
    
    def create_keyboard(self, parent_window):
        def on_key_press(key):
            entry_text.set(entry_text.get() + key)
        
        def save_name():
            print("ENTRY: ", entry.get())
            guardar = self.save_image(entry.get())
            if guardar:
                keyboard_window.destroy
                winBien = Toplevel(parent_window)
                winBien.title("Guardada")
                guardada = Label(winBien, text="La imagen ha sido guardada con exito").grid(row=0, column=0, padx=5, pady=5)

            else:
                winError = Toplevel(parent_window)
                winError.title("Error")
                noGuardada = Label(winError, text="No se ha guardado la imagen").grid(row=0, column=0, padx=5, pady=5)

        keyboard_window = Toplevel(parent_window)
        keyboard_window.title("Teclado")

        entry_text = StringVar()
        entry = Entry(keyboard_window, textvariable=entry_text)
        entry.grid(row=0, column=0, columnspan=8)

        btnEnviar = Button(keyboard_window, text="Aceptar",command=save_name)
        btnEnviar.grid(row=0, column=1)

        print("Nuevo nombre de la imagen: ", entry.get())

        buttons = [
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'ñ',
            'Z', 'X', 'C', 'V', 'B', 'N', 'M', '_', '', ''
        ]

        row = 1
        col = 0
        for button in buttons:
            if button == '':
                col += 1
                continue
            Button(keyboard_window, text=button, width=5, height=2,
                    command=lambda b=button: on_key_press(b)).grid(row=row, column=col)
            col += 1
            if col > 9: # Comprobar si ha cambiado de fila
                col = 0
                row += 1

    def open_keyboard(self):
        self.create_keyboard(self.master)


    def drawWidgets(self):

        screen_w, screen_h = pyautogui.size()

        self.controls = Frame(self.master, padx=5, pady=5)
        self.title = Label(self.controls, text="Opciones del Pincel", font='Gerorgia 14')
        self.title.grid(row=0,column=0, columnspan=3)

        #Grosor del pincel
        textpw = Label(self.controls, text='Grosor')
        textpw.grid(row=1, column=0,columnspan=3)

        self.slider = ttk.Scale(self.controls, from_=5, to=100, command = self.changedW, orient='horizontal')
        self.slider.set(self.pen_width)
        self.slider.grid(row=2, column=0, sticky="ew", columnspan=3)

        #Colores del pincel
        self.title_cambiar_color=Label(self.controls, text='pincel color',font='Gerorgia 14')
        self.title_cambiar_color.grid(row=3,column=0, columnspan=3)

        self.btn_cambiar_color_rojo=Button(self.controls, width=20,height=3, bg="#EF3737",command= lambda: self.change_fg(0))
        self.btn_cambiar_color_rojo.grid(row=4,column=0,padx=20, pady=10)

        self.btn_cambiar_color_azul=Button(self.controls, width=20,height=3, bg="#376AEF",command= lambda: self.change_fg(1))
        self.btn_cambiar_color_azul.grid(row=4,column=1,padx=20, pady=10)

        self.btn_cambiar_color_negro=Button(self.controls, width=20,height=3, bg="#000000",fg="#fff",command= lambda: self.change_fg(2))
        self.btn_cambiar_color_negro.grid(row=4,column=2,padx=20, pady=10)

        #Guardar adivinar
        self.title_guardar_adivianr=Label(self.controls, text='Guardar/Adivinar', font='Gerorgia 14')
        self.title_guardar_adivianr.grid(row=5,column=0, columnspan=3)

        self.btn_guardar=Button(self.controls, width=20,height=3 ,text="Guardar Imagen",command=self.open_keyboard)
        self.btn_guardar.grid(row=6,column=0,padx=20, pady=10)

        self.btn_borrar=Button(self.controls, width=20,height=3 ,text="Borrar lienzo",command=self.clearcanvas)
        self.btn_borrar.grid(row=6,column=1,padx=20, pady=10)

        self.btn_adivinar=Button(self.controls, width=20,height=3 ,text="Adivinar Imagen", command=self.usarModelo)
        self.btn_adivinar.grid(row=6,column=2,padx=20, pady=10)

        self.controls.grid(row=0,column=1, padx=20)

        self.c = Canvas(self.master, width=1200, height=1000, bg=self.color_bg)
        self.c.grid(row=0, column=0, sticky="ew", rowspan=2)

        self.btn_salir = Button(self.master, text="Salir", width=20,height=3 ,command=self.master.destroy)
        self.btn_salir.grid(row=2,column=1,padx=20, pady=5)

        menu = Menu(self.master)
        self.master.config(menu=menu)
        optionmenu = Menu(menu)
        menu.add_cascade(label='Menu', menu=optionmenu)
        optionmenu.add_command(label='pincel color', command=self.change_fg)
        optionmenu.add_command(label='fondo color', command=self.change_bg)
        optionmenu.add_command(label='Guardar Image', command=self.save_image)
        optionmenu.add_command(label='Borrar lienzo', command=self.clearcanvas)

    def update_camera(self):
        _, self.frame = self.cap.read()
        self.frame = cv2.flip(self.frame, 1)
        self.frame=detectarRostroVideo(self.frame)
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
        self.camera_label.configure(image=self.photo)
        self.camera_label.image = self.photo
        self.camera_label.after(10, self.update_camera)


    def usarModelo(self):
        def acertado(interfaz):
            datos= {"ejecucion": [{"num_intentos": 1}, {"resultado": latex[0]}]}

            guardarRespuestas(datos,interfaz)
        def fallado(interfaz):
            resultado = Toplevel(self.controls)
            resultado.title("Solución")
            preciccion  = Label(resultado, text="Es alguna de las siguientes opciones")
            preciccion.grid(row=0,column=0,columnspan=4)
            aux_colum=0
            for i in range(len(latex)):
                if i > 0:
                    Button(resultado, text=latex[i], command=lambda i=i:guardarRespuestas({"ejecucion": [{"num_intentos": 2}, {"resultado": latex[i]},{"predicho":latex[0]}]},interfaz),width=20, height=5).grid(row=1, column=aux_colum,padx=10, pady=10) #
                    aux_colum = aux_colum +1
        class_names = []
        # Nombre del archivo que contiene las palabras
        nombre_archivo = "./resources/mini_classes.txt"

        # Lee el contenido del archivo y crea una lista de palabras
        with open(nombre_archivo, 'r') as archivo:
            class_names = [line.strip() for line in archivo]

        # Obtener las dimensiones del canvas
        x0 = self.c.winfo_rootx()
        y0 = self.c.winfo_rooty()
        x1 = x0 + self.c.winfo_width()
        y1 = y0 + self.c.winfo_height()
        
        # Capturar el contenido del canvas como una imagen
        img_origin = ImageGrab.grab(bbox=(x0, y0, x1, y1))

        # Convertir la imagen a escala de grises
        img = img_origin.convert('L')

        image_size = 28
        model = tf.keras.models.load_model('resources/modelo.keras')
        
        # Redimensionar la imagen y convertirla en un array
        img_resized = img.resize((image_size, image_size))
        img_array = -(image.img_to_array(img_resized))
        plt.imshow(img_array.reshape(image_size, image_size), cmap='gray')
        plt.show()

        img_array = img_array.reshape(1, image_size, image_size, 1)
        img_array = img_array.astype('float32') / 255.0

        pred = model.predict(img_array)
        ind = (-pred).argsort()[0][:5]
        latex = [class_names[x] for x in ind]
        print("Top 5 predicciones:", latex)

        resultado = Toplevel(self.controls)
        resultado.title("Resultado")
        preciccion  = Label(resultado, text=latex[0])
        preciccion.grid(row=0, column=0, columnspan=2)
        opc1 = Button(resultado, text="si", command=lambda:acertado(self.controls),width=20, height=5)
        opc1.grid(row=1, column=0,padx=10, pady=10)
        opc2 = Button(resultado, text="no", command=lambda:fallado(self.controls),width=20, height=5)
        opc2.grid(row=1, column=1,padx=10, pady=10)

    

 

def empezar_paint():
    win = Tk()
    win.title("PAINT")
    win.attributes('-fullscreen', True)
    Pintura(win)
    win.mainloop()


empezar_paint()