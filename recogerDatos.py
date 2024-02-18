import json
import os
import tkinter as tk

def guardarRespuestas(nuevos_datos,interfaz):
    print(nuevos_datos)
    nombre_archivo = "datos.json"

    # Cargar datos existentes del archivo JSON
    if os.path.isfile(nombre_archivo) and os.path.getsize(nombre_archivo) > 0:
        # Cargar datos existentes del archivo JSON
        with open(nombre_archivo, "r") as archivo:
            datos_existente = json.load(archivo)
    else:
        # Si el archivo no existe o está vacío, inicializa los datos como una lista vacía
        datos_existente = []

    # Actualizar o añadir nuevos datos al diccionario existente
    datos_existente.append(nuevos_datos)

    # Guardar los datos actualizados en el JSON
    with open(nombre_archivo, "w") as archivo:
        json.dump(datos_existente, archivo)

    print("Datos guardados exitosamente.")

    for ventana in interfaz.winfo_children():
        if isinstance(ventana, tk.Toplevel):
            ventana.destroy()