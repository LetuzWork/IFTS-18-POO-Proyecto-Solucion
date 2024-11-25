from peewee import *
import pandas as pd
from abc import ABCMeta
import modelo_orm as orm

class GestionarObra(metaclass=ABCMeta):
    @classmethod
    def extraer_datos(cls):
        try:
            df = pd.read_csv('./observatorio-de-obras-urbanas.csv', sep=';', decimal=',', encoding='latin1', index_col=None)

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
            db.create_tables([orm.AreaResponsable, orm.Barrio, orm.Empresa, orm.Etapa,  orm.FuenteFinanciamiento, orm.TipoContratacion, orm.TipoObra, orm.Obra])
            print('Se han creado correctamente las tablas')
        except OperationalError as e:
            print(f'Se ha generado un error al crear las tablas: {e}')
            exit()
        db.close()
    
    # El codigo final del archivo limpieza se deberia implementar aca
    @classmethod
    def limpiar_datos(cls):
        df = cls.extraer_datos()
        columnas = ('nombre', 'etapa', 'tipo', 'area_responsable', 'monto_contrato', 'comuna', 'barrio', 'fecha_inicio', 'fecha_fin_inicial', 'plazo_meses', 'porcentaje_avance', 'licitacion_oferta_empresa', 'contratacion_tipo', 'nro_contratacion', 'mano_obra', 'destacada', 'expediente-numero', 'financiamiento')

        for column in df.columns:
            # Elimina todas las columnas no necesarias del dataframe
            if columnas.count(column) == 0:
                df = df.drop(columns=[column])
            # Elimina los valores nulos en todas las columnas consideradas importantes para el trabajo
            elif column == 'comuna' or column == 'barrio' or column == 'destacada':
                df = df.dropna(subset=[column])
                # Reindexa las columnas
                df = df.reset_index(drop=True)
            elif column == 'monto_contrato':
                df[column] = pd.to_numeric(df[column],errors='coerce')
                df = df.dropna(subset=[column])
                df = df.reset_index(drop=True)

        return df
    
    #parcialmente laburado en archivo limpieza
    @classmethod
    def cargar_datos(cls):
        df = cls.limpiar_datos()
        db = cls.conectar_db()

        # Guarda valores unicos en listas para poder cargarlos en las tablas que se relacionan con la tabla obra
        etapaUnique = list(df['etapa'].unique())
        tipoObraUnique = list(df['tipo'].unique())
        areaUnique = list(df['area_responsable'].unique())
        comunaUnique = list(df['comuna'].unique())
        barrioUnique = list(df['barrio'].unique())
        empresaUnique = list(df['licitacion_oferta_empresa'].unique())
        contratacionUnique = list(df['contratacion_tipo'].unique())
        financiamientoUnique = list(df['financiamiento'].unique())
        # // generamos esto con la funcion la funcion de generar unicos en archivo limpieza
        
        # // se puede crear una funcion para reducir la repeticion procurando
        # Cargamos los datos unicos en sus respectivas tablas y los persistimos en el modelo ORM
        for elem in etapaUnique:
            try:
                orm.Etapa.create(estado=elem)
            except IntegrityError as e:
                print(f'Error al insertar un nuevo registro en la tabla etapa: {e}')

        for elem in tipoObraUnique:
            try:
                orm.TipoObra.create(tipo=elem)
            except IntegrityError as e:
                print(f'Error al insertar un nuevo registro en la tabla tipo_obra: {e}')

        for elem in areaUnique:
            try:
                orm.AreaResponsable.create(area=elem)
            except IntegrityError as e:
                print(f'Error al insertar un nuevo registro en la tabla area_responsable: {e}')

        for elem in comunaUnique:
            try:
                orm.Comuna.create(numero=elem)
            except IntegrityError as e:
                print(f'Error al insertar un nuevo registro en la tabla comuna: {e}')
        
        for elem in barrioUnique:
            fila = df[df['barrio'] == elem]
            comuna = fila['comuna'].iloc[0]
            comuna_id = orm.Comuna.get(orm.Comuna.numero == comuna)

            try:
                orm.Barrio.create(nombre=elem, comuna_id=comuna_id.id)
            except IntegrityError as e:
                print(f'Error al insertar un nuevo registro en la tabla barrio: {e}')

        for elem in empresaUnique:
            try:
                orm.Empresa.create(nombre=elem)
            except IntegrityError as e:
                print(f'Error al insertar un nuevo registro en la tabla empresa: {e}')

        for elem in contratacionUnique:
            try:
                orm.TipoContratacion.create(tipo=elem)
            except IntegrityError as e:
                print(f'Error al insertar un nuevo registro en la tabla tipo_contratacion: {e}')

        for elem in financiamientoUnique:
            try:
                orm.FuenteFinanciamiento.create(fuente=elem)
            except IntegrityError as e:
                print(f'Error al insertar un nuevo registro en la tabla fuente_financiamiento: {e}')

        for elem in df.values:
            etapa = orm.Etapa.get(orm.Etapa.estado == elem[1])
            tipoObra = orm.TipoObra.get(orm.TipoObra.tipo == elem[2])
            areaResp = orm.AreaResponsable.get(orm.AreaResponsable.area == elem[3])
            comuna = orm.Comuna.get(orm.Comuna.numero == elem[5])
            barrio = orm.Barrio.get(orm.Barrio.nombre == elem[6])
            empresa = orm.Empresa.get(orm.Empresa.nombre == elem[11])
            tipoContr = orm.TipoContratacion.get(orm.TipoContratacion.tipo == elem[12])
            financiamiento = orm.FuenteFinanciamiento.get(orm.FuenteFinanciamiento.fuente == elem[17])
            
            try:
                orm.Obra.create(nombre=elem[0], monto_contrato=elem[4], fecha_inicio=elem[7], fecha_fin_inicial=elem[8], plazo_meses=elem[9], porcentaje_avance=elem[10], nro_contratacion=elem[13], mano_obra=elem[14], destacada=elem[15], nro_expediente=elem[16], etapa_id=etapa, tipo_obra_id=tipoObra, area_responsable_id=areaResp, comuna_id=comuna, barrio_id=barrio, empresa_id=empresa, tipo_contratacion_id=tipoContr, fuente_financiamiento_id=financiamiento)
            except IntegrityError as e:
                print(f'Error al insertar un nuevo registro en la tabla obra: {e}')
        
        db.close()

    @classmethod
    def nueva_obra(cls):
        db = cls.conectar_db()

        orm.Obra.nuevo_proyecto()
        orm.Obra.iniciar_contratacion()
        orm.Obra.adjudicar_obra()
        orm.Obra.iniciar_obra()
        orm.Obra.actualizar_porcentaje_avance()

        while True:
            respuesta = input('Desea incrementar el plazo de meses que lleva la obra en ejecución? (SI/NO): ')
            if respuesta == 'SI':
                orm.Obra.incrementar_plazo()
                break
            elif respuesta == 'NO':
                break
            else:
                print('La respuesta no es valida.\nIngresar la respuesta nuevamente')

        while True:
            respuesta = input('Desea incrementar la mano de obra? (SI/NO): ')
            if respuesta == 'SI':
                orm.Obra.incrementar_mano_obra()
                break
            elif respuesta == 'NO':
                break
            else:
                print('La respuesta no es valida.\nIngresar la respuesta nuevamente')

        while True:
            respuesta = int(input('Desea:\n1. Finalizar la obra\n2. Rescindir la obra\n: '))
            if respuesta == 1:
                orm.Obra.finalizar_obra()
                break
            elif respuesta == 2:
                orm.Obra.rescindir_obra()
                break
            else:
                print('La respuesta no es valida.\nIngresar la respuesta nuevamente')

        db.close()

    @classmethod
    def obtener_indicadores(cls):
        db = cls.conectar_db()

        try:
            # a. Listado de todas las áreas responsables
            print('\nListado de áreas responsables:')
            for area in orm.AreaResponsable.select():
                print(area)

            # b. Listado de todos los tipos de obra
            print('\nListado de tipos de obra:')
            for tipo_obra in orm.TipoObra.select():
                print(tipo_obra)

            # c. Cantidad de obras que se encuentran en cada etapa
            print('\nCantidad de obras por etapa:')
            for etapa in orm.Etapa.select():
                cantidad_obras = orm.Obra.select().where(orm.Obra.etapa == etapa).count()
                print(f'{etapa.estado}: {cantidad_obras} obras')

            # d. Cantidad de obras y monto total de inversión por tipo de obra
            print('\nCantidad de obras y monto total de inversión por tipo de obra:')
            for tipo_obra in orm.TipoObra.select():
                obras = orm.Obra.select().where(orm.Obra.tipo_obra == tipo_obra)
                cantidad_obras = obras.count()
                monto_total = obras.select(fn.SUM(orm.Obra.monto_contrato)).scalar() or 0
                
                print(f'-{tipo_obra.tipo}: {cantidad_obras} obras, Monto total de inversión: ${monto_total:,.2f}')
            
            # e. Listado de todos los barrios pertenecientes a las comunas 1, 2 y 3
            print('\nListado de todos los barrios pertenecientes a las comunas 1, 2 y 3:')
            barrios = orm.Barrio.select().where(orm.Barrio.comuna <= 3)
            
            print('\n'.join(barrio.nombre for barrio in barrios))
            
            # f. Cantidad de obras finalizadas y su monto total de inversión en la comuna 1
            print('\nObras finalizadas y su monto total de inversión en la comuna 1:')
            obras_finalizadas_c1 = orm.Obra.select().join(orm.Barrio).join(orm.Etapa).where((orm.Etapa.nombre == 'Finalizada') & (orm.Barrio.comuna == 1))
            cantidad_obras_c1 = obras_finalizadas_c1.count()
            monto_total_c1 = obras_finalizadas_c1.select(fn.SUM(orm.Obra.monto_contrato)).scalar() or 0
            
            print(f'Cantidad de obras: {cantidad_obras_c1}')
            print(f'Monto total de inversión: ${monto_total_c1:,.2f}')

            # g. Cantidad de obras finalizadas en un plazo menor o igual a 24 meses
            print('\nCantidad de obras finalizadas en un plazo menor o igual a 24 meses:')
            obras_finalizadas_plazo = orm.Obra.select().join(orm.Etapa).where((orm.Etapa.nombre == 'Finalizada') & (orm.Obra.plazo_meses <= 24)).count()
            
            print(f'\nObras finalizadas en un plazo menor o igual a 24 meses: {obras_finalizadas_plazo}')
        
            # h. Porcentaje total de obras finalizadas
            print('\nPorcentaje total de obras finalizadas:')
            total_obras = orm.Obra.select().count()
            obras_finalizadas = orm.Obra.select().join(orm.Etapa).where(orm.Etapa.nombre == 'Finalizada').count()
            porcentaje_obras_finalizadas = (obras_finalizadas / total_obras) * 100 if total_obras > 0 else 0
            
            print(f'\nPorcentaje de obras finalizadas: {porcentaje_obras_finalizadas:.2f}%')

            # i. Cantidad total de mano de obra empleada
            print('\nCantidad total de mano de obra empleada:')
            cantidad_total = orm.Obra.select(fn.SUM(orm.Obra.mano_obra)).scalar() or 0
            
            print(f'\nCantidad total de mano de obra empleada: {cantidad_total:,}')

            # j. Monto total de inversión
            print('\nMonto total de inversión:')
            monto_total_inversion = orm.Obra.select(fn.SUM(orm.Obra.monto_contrato)).scalar() or 0
            
            print(f"Monto total de inversion: ${monto_total_inversion:,.2f}")

        except Exception as e:
            print(f"Error al obtener indicadores: {e}")
        finally:
            db.close()

if __name__ == '__main__':
    #GestionarObra().mapear_orm()
    #GestionarObra().limpiar_datos()
    #GestionarObra().cargar_datos()
    
    while True:
        respuesta = input('\nDesea crear una nueva instancia de obra? (SI/NO): ')

        if respuesta == 'SI':
            GestionarObra().nueva_obra()
        elif respuesta == 'NO':
            break
        else:
            print('La respuesta no es valida.\nIngresar la respuesta nuevamente')
    
    print('\nAquí estan los datos solicitados:')
    GestionarObra().obtener_indicadores()