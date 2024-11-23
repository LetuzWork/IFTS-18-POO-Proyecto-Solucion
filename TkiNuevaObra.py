import tkinter as tk
from tkinter import ttk
import Limpieza as lim
import pandas as pd
import GestionarObra

# Crear la ventana principal
root = tk.Tk()
root.title("Crear Nueva Obra")

# Crear los campos de entrada
fields = ['nombre', 'etapa', 'tipo', 'area_responsable', 'monto_contrato', 'comuna', 'barrio', 'fecha_inicio', 'fecha_fin_inicial', 'plazo_meses', 'porcentaje_avance', 'licitacion_oferta_empresa', 'contratacion_tipo', 'nro_contratacion', 'mano_obra', 'destacada', 'expediente_numero', 'financiamiento']
entries = {}

for field in fields:
    frame = tk.Frame(root)
    frame.pack(fill='x')
    label = tk.Label(frame, text=field, width=20, anchor='w')
    label.pack(side='left')
    entry = tk.Entry(frame)
    entry.pack(side='left', fill='x', expand=True)
    entries[field] = entry

# Función para obtener los datos de los campos y crear una nueva obra
def crear_obra():
    datos = {field: entry.get() for field, entry in entries.items()}
    GestionarObra.nueva_obra(**datos)

# Botón para crear la obra
btn_crear = tk.Button(root, text="Crear Obra", command=crear_obra)
btn_crear.pack(pady=10)

# Iniciar el bucle principal de la aplicación
root.mainloop()