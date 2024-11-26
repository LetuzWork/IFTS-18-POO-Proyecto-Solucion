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
        df = df.drop_duplicates(subset='cuit_contratista', keep='first') # Eliminar duplicados por cuit_contratista (A revisar)
        
        try:
            for _, row in df.iterrows():
            # Crear o obtener instancias de los modelos relacionados
                area_responsable, _ = orm.AreaResponsable.get_or_create(nombre=row['area_responsable'])
                barrio, _ = orm.Barrio.get_or_create(nombre=row['barrio'], comuna=row['comuna'])
                tipo_obra, _ = orm.TipoObra.get_or_create(nombre=row['tipo'])
                etapa, _ = orm.Etapa.get_or_create(nombre=row['etapa'])
                fuente_financiamiento, _ = orm.FuenteFinanciamiento.get_or_create(nombre=row['financiamiento'])
                tipo_contratacion, _ = orm.TipoContratacion.get_or_create(nombre=row['contratacion_tipo'])
                empresa, _ = orm.Empresa.get_or_create(nombre=row['licitacion_oferta_empresa'], cuit=row['cuit_contratista'],defaults={'nombre': row['licitacion_oferta_empresa']})

            for _, row in df.iterrows():
                orm.Obra.create(
                    tipo_obra=tipo_obra,
                    area_responsable=area_responsable,
                    barrio=barrio,
                    destacada=False,
                    fecha_inicio=row['fecha_inicio'],
                    fecha_fin_inicial=row['fecha_fin_inicial'],
                    porcentaje_avance=row['porcentaje_avance'],
                    plazo_meses=row['plazo_meses'],
                    mano_obra=row['mano_obra'],
                    etapa=etapa,
                    tipo_contratacion=tipo_contratacion,
                    nro_contratacion=row['nro_contratacion'],
                    empresa=empresa,
                    expediente_numero=row['expediente-numero'],
                    fuente_financiamiento=fuente_financiamiento,
                    nombre=row['nombre'],
                    monto_contrato=row['monto_contrato'],
                )
            print("Datos cargados exitosamente a la base de datos.")
        except Exception as e:
            print(f"Error al cargar datos: {e}")
        finally:
            db.close()

    @classmethod
    def nueva_obra(cls):
        print("En Proceso")

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
    GestionarObra.cargar_datos()
    
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