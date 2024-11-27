#Crear una ventana principal con tk inter con los colores que estan comentados en el codigo anterior. Hace que los colores sean variables globales. Los datos se sacaran de un df de pandas que lea el csv datos_limpios.
# El título será 'Sistema de Gestión de Obras Públicas de la Ciudad de Buenos Aires' y la ventana será redimensionable. En una tabla se mostrarán las obras de la base de datos obras_urbanas.db: id, nombre, barrio, comuna. Se podrá filtrar por barrio y buscar por nombre o palabra clave. Se podrá ver los detalles de la obra seleccionada con un botón 'Ver Detalles'. Se podrá ver los detalles de una obra seleccionada con un diseño jerarquico de titulo, descripción, barrio, comuna, área responsable, monto del contrato, empresa, financiación y si es destacada. Se podrá crear una nueva obra con un botón que abrirá una subventana con un label 'Ingrese los datos de la nueva obra'. Se podrá gestionar una obra con un botón que abrirá una subventana con un label 'Ingrese el ID de la obra a gestionar'.  Se podrá buscar obras por nombre o palabra clave con un botón 'Buscar'. Se podrá filtrar obras. 

from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import pandas as pd

dfou = pd.read_csv('datos_limpios.csv')

BG_COLOR = '#FAF0E4'
HEADER_COLOR = '#FFCD38'
BUTTON_COLOR = '#FF8551'
TEXT_COLOR = '#FAF0E4'

# Crear una ventana principal
root = tk.Tk()
root.geometry('800x600')
root.configure(bg=BG_COLOR)
root.title('Sistema de Gestión de Obras Públicas de la Ciudad de Buenos Aires')
root.resizable(True, True)

# Crear un marco para el logo en la cabecera
logo_frame = tk.Frame(root, width=600, height=22, bg=HEADER_COLOR)
logo_frame.pack(fill='x')
logo_frame.pack_propagate(False)

# Crear un marco para la cabecera
header_frame = tk.Frame(root, width=600, height=250, bg=BG_COLOR)
header_frame.pack(fill='x')
header_frame.pack_propagate(False)

# Cargar la imagen
obraurbana_img = tk.PhotoImage(file='obraurbana.png')

# Crear un título grande
titulo_label = tk.Label(header_frame, text='Obras Urbanas de la Ciudad de Buenos Aires', bg=BG_COLOR, font=("Helvetica", 24, "bold"))
titulo_label.pack(pady=10)
# Crear un label para la imagen y agregarlo al marco de la cabecera
img_label = tk.Label(header_frame, image=obraurbana_img, bg=BG_COLOR)
img_label.pack(pady=10)


# Función para ver detalles de la obra seleccionada
def ver_detalles_obra():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione una obra para ver los detalles.")
        return
    

    obra_nombre = tree.item(selected_item)['values'][0]
    obra = dfou[dfou['nombre'] == obra_nombre].iloc[0]

    detalles_obra = tk.Toplevel(root)
    detalles_obra.title(f"Detalles de la Obra: {obra['nombre']}")
    detalles_obra.geometry('400x400')
    detalles_obra.configure(bg=BG_COLOR)

     # Crear y agregar los labels con el formato solicitado
    nombre_label = tk.Label(detalles_obra, text=f"Nombre: {obra['nombre']}", bg=BG_COLOR, font=("Helvetica", 16, "bold"))
    nombre_label.pack(pady=5)

    descripcion_label = tk.Label(detalles_obra, text=f"Descripción: {obra['descripcion']}", bg=BG_COLOR, wraplength=300, justify='center')
    descripcion_label.pack(pady=5)

    barrio_label = tk.Label(detalles_obra, text=f"Barrio: {obra['barrio']}", bg=BG_COLOR, font=("Helvetica", 10, "bold"))
    barrio_label.pack(pady=5)

    comuna_label = tk.Label(detalles_obra, text=f"Comuna: {obra['comuna']}", bg=BG_COLOR, font=("Helvetica", 10, "bold"))
    comuna_label.pack(pady=5)

    area_responsable_label = tk.Label(detalles_obra, text=f"Área Responsable: {obra['area_responsable']}", bg=BG_COLOR, font=("Helvetica", 10, "underline"))
    area_responsable_label.pack(pady=5)

    monto_contrato_label = tk.Label(detalles_obra, text=f"Monto del Contrato: ${obra['monto_contrato']}", bg=BG_COLOR, fg=BUTTON_COLOR)
    monto_contrato_label.pack(pady=5)

    
# Crear una tabla (Treeview)
tree = ttk.Treeview(root, columns=('Nombre', 'Barrio', 'Área Responsable'), show='headings')
tree.heading('Nombre', text='Nombre')
tree.heading('Barrio', text='Barrio')
tree.column('Barrio', width=100)  # Ajustar el ancho de la columna Barrio
tree.heading('Área Responsable', text='Área Responsable')

# Insertar datos en la tabla
for index, row in dfou.iterrows():
    tree.insert('', 'end', text=row['nombre'], values=(row['nombre'], row['barrio'], row['area_responsable']))

tree.pack(pady=10)

# Crear un botón para ver detalles de la obra seleccionada
details_button = tk.Button(root, text='Ver Detalles', command=ver_detalles_obra, bg=BUTTON_COLOR, fg=TEXT_COLOR)
details_button.pack(pady=10)

# Cargar datos en el combobox de obras
obras = dfou['nombre'].tolist()

# Función para mostrar detalles de la obra seleccionada
def mostrar_detalles_obra(event):
    obra_nombre = obras.get()
    obra = dfou[dfou['nombre'] == obra_nombre].iloc[0]
    # Filtrar las obras por el barrio seleccionado
    filtered_df = dfou[dfou['barrio'] == obra_nombre]

    # Limpiar la tabla antes de insertar nuevos datos
    for item in tree.get_children():
        tree.delete(item)

    # Insertar los datos filtrados en la tabla
    for index, row in filtered_df.iterrows():
        tree.insert('', 'end', text=row['nombre'], values=(row['nombre'], row['barrio'], row['area_responsable']))
    detalles_text = f"""
    Nombre: {obra['nombre']}
    Descripción: {obra['descripcion']}
    Barrio: {obra['barrio']}
    Comuna: {obra['comuna']}
    Área Responsable: {obra['area_responsable']}
    Monto del Contrato: ${obra['monto_contrato']}
    Financiación: {obra['financiacion']}
    Destacada: {'Sí' if obra['destacada'] else 'No'}
    """

    detalles_label.config(text=detalles_text)

# Crear un label para mostrar los detalles de la obra
detalles_label = tk.Label(root, text='', bg=BG_COLOR, justify='left')
detalles_label.pack(pady=10)



root.mainloop()