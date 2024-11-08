from peewee import *

import sys

# Conexión a la base de datos SQLite
db = SqliteDatabase('empleados.db')

class BaseModel(Model):
    class Meta:
        database = db

class Area(BaseModel):
    nombre_area = CharField(unique=True, max_length=80)

class Empleado(BaseModel):
    nro_legajo = IntegerField(unique=True)
    dni = IntegerField(unique=True)
    nombre = CharField()
    apellido = CharField()
    area = ForeignKeyField(Area, backref='empleados')

# Crear las tablas
db.connect()
db.create_tables([Area, Empleado])

def insertar_empleado():
    try:
        nro_legajo = int(input("Ingrese el número de legajo: "))
        dni = int(input("Ingrese el DNI: "))
        nombre = input("Ingrese el nombre: ")
        apellido = input("Ingrese el apellido: ")
        nombre_area = input("Ingrese el nombre del área: ")

        area, created = Area.get_or_create(nombre_area=nombre_area)
        Empleado.create(nro_legajo=nro_legajo, dni=dni, nombre=nombre, apellido=apellido, area=area)
        print("Empleado insertado correctamente.")
    except IntegrityError as e:
        print(f"Error al insertar el empleado: {e}")

def seleccionar_empleado_por_dni():
    try:
        dni = int(input("Ingrese el DNI del empleado: "))
        empleado = Empleado.get(Empleado.dni == dni)
        print(f"Empleado encontrado: {empleado.nombre} {empleado.apellido}, Área: {empleado.area.nombre_area}")
    except DoesNotExist:
        print("Empleado no encontrado.")

def seleccionar_todos_los_empleados():
    empleados = Empleado.select()
    for empleado in empleados:
        print(f"{empleado.nro_legajo} - {empleado.nombre} {empleado.apellido}, Área: {empleado.area.nombre_area}")

def modificar_area_empleado():
    try:
        nro_legajo = int(input("Ingrese el número de legajo del empleado: "))
        nuevo_nombre_area = input("Ingrese el nuevo nombre del área: ")

        empleado = Empleado.get(Empleado.nro_legajo == nro_legajo)
        nueva_area, created = Area.get_or_create(nombre_area=nuevo_nombre_area)
        empleado.area = nueva_area
        empleado.save()
        print("Área del empleado modificada correctamente.")
    except DoesNotExist:
        print("Empleado no encontrado.")
    except IntegrityError as e:
        print(f"Error al modificar el área del empleado: {e}")

def eliminar_empleado():
    try:
        nro_legajo = int(input("Ingrese el número de legajo del empleado: "))
        empleado = Empleado.get(Empleado.nro_legajo == nro_legajo)
        empleado.delete_instance()
        print("Empleado eliminado correctamente.")
    except DoesNotExist:
        print("Empleado no encontrado.")

def main():
    while True:
        print("\nOpciones:")
        print("1. Insertar un registro de empleado.")
        print("2. Seleccionar un registro de empleado a partir de su número DNI.")
        print("3. Seleccionar todos los empleados o los registros de la tabla.")
        print("4. Modificar el área de un empleado en función de su número de legajo.")
        print("5. Eliminar un empleado a partir del número de legajo.")
        print("6. Finalizar.")

        opcion = input("Ingrese una opción: ")

        if opcion == '1':
            insertar_empleado()
        elif opcion == '2':
            seleccionar_empleado_por_dni()
        elif opcion == '3':
            seleccionar_todos_los_empleados()
        elif opcion == '4':
            modificar_area_empleado()
        elif opcion == '5':
            eliminar_empleado()
        elif opcion == '6':
            print("Finalizando...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()