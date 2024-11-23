import tkinter as tk
from tkinter import ttk
import Limpieza as lim
import pandas as pd
from PIL import Image, ImageTk

# Supongamos que tienes un DataFrame llamado dftrim con las columnas 'nombre' y 'descripcion'
dftrim = pd.DataFrame(lim.dftk, columns=['nombre', 'descripcion', 'imagen_1'])

# Función para actualizar la descripción cuando se selecciona una obra
def actualizar_descripcion(event):
    obra_seleccionada = combobox.get()
    descripcion = dftrim[dftrim['nombre'] == obra_seleccionada]['descripcion'].values[0]
    label_descripcion.config(text=descripcion)
    ruta = dftrim[dftrim['nombre'] == obra_seleccionada]['imagen_1'].values[0]
    label_imagen.config(image=ImageTk.PhotoImage(Image.open(ruta)))
    root.title(obra_seleccionada)  # Actualizar el título de la ventana con el nombre de la obra


# Crear la ventana principal
root = tk.Tk()
root.title("Seleccionar Obra")

# Crear el combobox para seleccionar la obra
combobox = ttk.Combobox(root, values=dftrim['nombre'].tolist())
combobox.bind("<<ComboboxSelected>>", actualizar_descripcion)
combobox.pack(pady=10)

# Crear un widget Label para mostrar la imagen
label_imagen = tk.Label(root)
label_imagen.pack(pady=10)


# Crear una etiqueta para mostrar la descripción
label_descripcion = tk.Label(root, text="", wraplength=300)
label_descripcion.pack(pady=10)

# Iniciar el bucle principal de la aplicación
root.mainloop()