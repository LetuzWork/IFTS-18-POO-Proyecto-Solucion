from peewee import *
import pandas as pd
from abc import ABCMeta
import modelo_orm as orm
from utils import limpiar_columnas, columnas_interes

class GestionarObra(metaclass=ABCMeta):
    @classmethod
    def extraer_datos(cls):
        try:
            df = pd.read_csv('./observatorio-de-obras-urbanas.csv', sep=";", index_col=0, encoding='latin-1').reset_index(drop=True)

            return df
        except FileNotFoundError as e:
            print(f'Error al conectar con el dataset: {e}')
            return False

    @classmethod
    def conectar_db(cls):
        try:
            db = SqliteDatabase('obras_urbanas.db', pragmas ={'journal_mode' : 'wal'})
            db.connect()
            print('Se conectó correctamente a la base de datos')
            return db
        except OperationalError as e:
            print(f'Error al conectar con la base: {e}')
            exit()

    @classmethod
    def mapear_orm(cls):
        db = cls.conectar_db()
        try:
            db.create_tables([orm.AreaResponsable, orm.Barrio, orm.Empresa, orm.Etapa, orm.FuenteFinanciamiento, orm.TipoContratacion, orm.TipoObra, orm.Obra])
            print('Se han creado correctamente las tablas')
        except OperationalError as e:
            print(f'Se ha generado un error al crear las tablas: {e}')
            exit()
        db.close()
    
    @classmethod
    def limpiar_datos(cls):
        df = cls.extraer_datos()
        df = limpiar_columnas(df[columnas_interes])
        return df

    @classmethod
    def cargar_datos(cls):
        df = cls.limpiar_datos()
        db = cls.conectar_db()

        print("Codigo de Cargado de datos en proceso")
        
        db.close()

    @classmethod
    def nueva_obra(cls):
        db = cls.conectar_db()
        cls.mapear_orm()
        
        try:
            nombre = input("\nIngrese el nombre de la obra:")
            monto_contrato = float(input("\nIngrese el monto de contrato:"))
            fec_inicio = input("\nIngrese la fecha de inicio (YYYY-MM-DD):")
            fec_final = input("\nIngrese la fecha de finalización (YYYY-MM-DD):")
            plazo_meses = int(input("\nIngrese el plazo en meses:"))
            porcentaje_avance = float(input("\nIngrese el porcentaje de avance:"))
            num_contratacion = input("\nIngrese el número de contratación:")
            mano_obra = int(input("\nIngrese la cantidad de mano de obra:"))
            expediente_numero = input("\nIngrese la número de expediente:")
            
            destacada = None  
            while destacada is None:
                respuesta = input("\nLa obra es destacada? (SI/NO): ").strip().upper()
                if respuesta == "SI":
                    destacada = True
                elif respuesta == "NO":
                    destacada = False
                else:
                    print("Respuesta no válida. Por favor ingrese 'SI' o 'NO'.")


            def obtener_instancia(tabla, columna, mensaje):

                while True:
                    valor = input(f"\n{mensaje}: ").strip()
                    try:
                        instancia = tabla.get_or_create(**{columna: valor}) 
                        return instancia[0]
                    except tabla.DoesNotExist:
                        print(f"No se encontró un registro en {tabla._meta.table_name} con {columna}='{valor}'. Intente nuevamente.")
            
            
            def obtener_instancia_compleja(tabla, columna, mensaje, columna_secundaria, mensaje_columna_secundaria):
                
                while True:
                    valor = input(f"\n{mensaje}: ").strip()
                    try:
                        instancia = tabla.get(**{columna: valor}) 
                        return instancia
                    except tabla.DoesNotExist:
                        valor_secundario = input(f"\n{mensaje_columna_secundaria}: ").strip()
                        try:
                            instancia = tabla.get_or_create(**{columna: valor, columna_secundaria: valor_secundario}) 
                            return instancia[0]
                        # except tabla.ValueError:
                        #     instancia = tabla.get_or_create(**{columna: valor, columna_secundaria: int(valor_secundario)}) 
                        #     return instancia
                        except tabla.DoesNotExist:
                            print(f"No se encontró un registro en {tabla._meta.table_name} con {columna_secundaria}='{valor_secundario}'. Intente nuevamente.")
                    except Exception as e:
                        # Mostrar el tipo de excepción y el mensaje
                        print(f"Se produjo una excepción de tipo: {type(e).__name__}")

            tipo_obra = obtener_instancia(orm.TipoObra, "nombre", "Ingrese el tipo de obra") 
            area_responsable = obtener_instancia(orm.AreaResponsable, "nombre", "Ingrese el área responsable")
            etapa = obtener_instancia(orm.Etapa, "nombre", "Ingrese la etapa inicial")
            tipo_contratacion = obtener_instancia(orm.TipoContratacion, "nombre", "Ingrese el tipo de contratación")
            fuente_financiamiento = obtener_instancia(orm.FuenteFinanciamiento, "nombre", "Ingrese la fuente de financiamiento")
            empresa = obtener_instancia_compleja(orm.Empresa, "nombre", "Ingrese el nombre de la empresa", "cuit", "Ingrese el número de CUIT")
            barrio = obtener_instancia_compleja(orm.Barrio, "nombre", "Ingrese el nombre del barrio", "comuna", "Ingrese el número de la comuna")

            nueva_obra = orm.Obra(
            nombre=nombre,
            monto_contrato=monto_contrato,
            fecha_inicio=fec_inicio,
            fecha_fin_inicial=fec_final,
            plazo_meses=plazo_meses,
            porcentaje_avance=porcentaje_avance,
            nro_contratacion=num_contratacion,
            mano_obra=mano_obra,
            destacada=destacada,
            expediente_numero=expediente_numero,
            tipo_obra=tipo_obra,
            area_responsable=area_responsable,
            barrio=barrio,
            etapa=etapa,
            tipo_contratacion=tipo_contratacion,
            empresa=empresa,
            fuente_financiamiento=fuente_financiamiento
        )

            obra = orm.Obra.create(nombre = nombre, monto_contrato=monto_contrato)

            obra.nuevo_proyecto(tipo_obra, area_responsable, barrio)

            obra.iniciar_contratacion(tipo_contratacion, num_contratacion)

            obra.adjudicar_obra(empresa, expediente_numero) 

            obra.iniciar_obra(destacada, fec_inicio, fec_final, fuente_financiamiento, mano_obra)

            obra.actualizar_porcentaje_avance(porcentaje_avance)

            accion_final = None
            while accion_final is None:
                respuesta = input("\n¿Quieres rescindir la obra o darla por finalizada? (SI/NO): ").strip().upper()
                if respuesta == "SI":
                    accion_final = True
                    obra.rescindir_obra()
                elif respuesta == "NO":
                    accion_final = False
                    obra.finalizar_obra()
                else:
                    print("Respuesta no válida. Por favor ingrese 'SI' o 'NO'.")


        except Exception as e:
            print(f"Error al crear la obra: {e}  {type(e).__name__}")
            return None
        

    @classmethod
    def obtener_indicadores(cls):
        db = cls.conectar_db()

        try:
            # a. Listado de todas las áreas responsables
            print('\nListado de áreas responsables:')
            print("\n".join(area.nombre for area in orm.AreaResponsable.select()))

            # b. Listado de todos los tipos de obra
            print('\nListado de tipos de obra:')
            print("\n".join(tipo_obra.nombre for tipo_obra in orm.TipoObra.select()))

            # c. Cantidad de obras que se encuentran en cada etapa
            print('\nCantidad de obras por etapa:')
            for etapa in orm.Etapa.select():
                cantidad_obras = orm.Obra.select().where(orm.Obra.etapa == etapa).count()
                print(f'{etapa.nombre}: {cantidad_obras} obras')

            # d. Cantidad de obras y monto total de inversión por tipo de obra
            print('\nCantidad de obras y monto total de inversión por tipo de obra:')
            for tipo_obra in orm.TipoObra.select():
                obras = orm.Obra.select().where(orm.Obra.tipo_obra == tipo_obra)
                cantidad_obras = obras.count()
                monto_total = obras.select(fn.SUM(orm.Obra.monto_contrato)).scalar() or 0
                
                print(f'{tipo_obra.nombre}: {cantidad_obras} obra/s, Monto total de inversión: ${monto_total:,.2f}')
            
            # e. Listado de todos los barrios pertenecientes a las comunas 1, 2 y 3
            print('\nListado de todos los barrios pertenecientes a las comunas 1, 2 y 3:')
            barrios = orm.Barrio.select().where(orm.Barrio.comuna <= 3)
            
            print('\n'.join(barrio.nombre for barrio in barrios) if len(barrios) else "Ninguna")
            
            # f. Cantidad de obras finalizadas y su monto total de inversión en la comuna 1
            print('\nEn la comuna 1:')
            obras_finalizadas_c1 = orm.Obra.select().join(orm.Barrio).switch(orm.Obra).join(orm.Etapa).where((orm.Etapa.nombre == 'Finalizada') & (orm.Barrio.comuna == 1))

            cantidad_obras_c1 = obras_finalizadas_c1.count()
            monto_total_c1 = obras_finalizadas_c1.select(fn.SUM(orm.Obra.monto_contrato)).scalar() or 0
            
            print(f'Cantidad de obras finalizadas: {cantidad_obras_c1}')
            print(f'Monto total de inversión: ${monto_total_c1:,.2f}')

            # g. Cantidad de obras finalizadas en un plazo menor o igual a 24 meses
            obras_finalizadas_plazo = orm.Obra.select().join(orm.Etapa).where((orm.Etapa.nombre == 'Finalizada') & (orm.Obra.plazo_meses <= 24)).count()
            
            print(f'\nObras finalizadas en un plazo menor o igual a 24 meses: {obras_finalizadas_plazo}')
        
            # h. Porcentaje total de obras finalizadas
            total_obras = orm.Obra.select().count()
            obras_finalizadas = orm.Obra.select().join(orm.Etapa).where(orm.Etapa.nombre == 'Finalizada').count()
            porcentaje_obras_finalizadas = (obras_finalizadas / total_obras) * 100 if total_obras > 0 else 0
            
            print(f'\nPorcentaje de obras finalizadas: {porcentaje_obras_finalizadas:.2f}%')

            # i. Cantidad total de mano de obra empleada
            cantidad_total = orm.Obra.select(fn.SUM(orm.Obra.mano_obra)).scalar() or 0
            
            print(f'\nCantidad total de mano de obra empleada: {cantidad_total:,.2f}')

            # j. Monto total de inversión
            monto_total_inversion = orm.Obra.select(fn.SUM(orm.Obra.monto_contrato)).scalar() or 0
            
            print(f"Monto total de inversion: ${monto_total_inversion:,.2f}")

        except Exception as e:
            print(f"Error al obtener indicadores: {e}")
        finally:
            db.close()

if __name__ == '__main__':
    GestionarObra.mapear_orm()
    # GestionarObra.cargar_datos()
    
    # while True:
    #     respuesta = input('\nDesea crear una nueva instancia de obra? s/n: ')

    #     if respuesta.lower() == 's':
    #         GestionarObra.nueva_obra()
    #     elif respuesta.lower() == 'n':
    #         break
    #     else:
    #         print('La respuesta no es valida.\nIngresar la respuesta nuevamente')
    
    # print('\nAquí estan los datos solicitados:')
    # GestionarObra.obtener_indicadores()
    
    GestionarObra.nueva_obra()
