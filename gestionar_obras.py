from peewee import *
import pandas as pd
from abc import ABCMeta
import modelo_orm
db = SqliteDatabase('obras_urbanas.db', pragmas ={'journal_mode' : 'wal'})
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
            db = sqlite_db.connect('obras_urbanas.db')
            print('Se conectó correctamente a la base de datos')
            return db
        except OperationalError as e:
            print(f'Error al conectar con la base: {e}')
            exit()

    @classmethod
    def mapear_orm(cls):
        db = cls.conectar_db()
        try:
            db.create_tables([modelo_orm.AreaResponsable, modelo_orm.Barrio, modelo_orm.Empresa, modelo_orm.Etapa,  modelo_orm.FuenteFinanciamiento, modelo_orm.TipoContratacion, modelo_orm.TipoObra, modelo_orm.Obra])
            print('Se han creado correctamente las tablas')
        except OperationalError as e:
            print(f'Se ha generado un error al crear las tablas: {e}')
            exit()
        sqlite_db.close()
    
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
        // generamos esto con la funcion la funcion de generar unicos en archivo limpieza
        
        // se puede crear una funcion para reducir la repeticion procurando
        # Cargamos los datos unicos en sus respectivas tablas y los persistimos en el modelo ORM
        for elem in etapaUnique:
            try:
                modelo_orm.Etapa.create(estado=elem)
            except IntegrityError as e:
                print(f'Error al insertar un nuevo registro en la tabla etapa: {e}')

        for elem in tipoObraUnique:
            try:
                modelo_orm.TipoObra.create(tipo=elem)
            except IntegrityError as e:
                print(f'Error al insertar un nuevo registro en la tabla tipo_obra: {e}')

        for elem in areaUnique:
            try:
                modelo_orm.AreaResponsable.create(area=elem)
            except IntegrityError as e:
                print(f'Error al insertar un nuevo registro en la tabla area_responsable: {e}')

        for elem in comunaUnique:
            try:
                modelo_orm.Comuna.create(numero=elem)
            except IntegrityError as e:
                print(f'Error al insertar un nuevo registro en la tabla comuna: {e}')
        
        for elem in barrioUnique:
            fila = df[df['barrio'] == elem]
            comuna = fila['comuna'].iloc[0]
            comuna_id = modelo_orm.Comuna.get(modelo_orm.Comuna.numero == comuna)

            try:
                modelo_orm.Barrio.create(nombre=elem, comuna_id=comuna_id.id)
            except IntegrityError as e:
                print(f'Error al insertar un nuevo registro en la tabla barrio: {e}')
          
        for elem in empresaUnique:
            try:
                modelo_orm.Empresa.create(nombre=elem)
            except IntegrityError as e:
                print(f'Error al insertar un nuevo registro en la tabla empresa: {e}')

        for elem in contratacionUnique:
            try:
                modelo_orm.TipoContratacion.create(tipo=elem)
            except IntegrityError as e:
                print(f'Error al insertar un nuevo registro en la tabla tipo_contratacion: {e}')

        for elem in financiamientoUnique:
            try:
                modelo_orm.FuenteFinanciamiento.create(fuente=elem)
            except IntegrityError as e:
                print(f'Error al insertar un nuevo registro en la tabla fuente_financiamiento: {e}')

        for elem in df.values:
            etapa = modelo_orm.Etapa.get(modelo_orm.Etapa.estado == elem[1])
            tipoObra = modelo_orm.TipoObra.get(modelo_orm.TipoObra.tipo == elem[2])
            areaResp = modelo_orm.AreaResponsable.get(modelo_orm.AreaResponsable.area == elem[3])
            comuna = modelo_orm.Comuna.get(modelo_orm.Comuna.numero == elem[5])
            barrio = modelo_orm.Barrio.get(modelo_orm.Barrio.nombre == elem[6])
            empresa = modelo_orm.Empresa.get(modelo_orm.Empresa.nombre == elem[11])
            tipoContr = modelo_orm.TipoContratacion.get(modelo_orm.TipoContratacion.tipo == elem[12])
            financiamiento = modelo_orm.FuenteFinanciamiento.get(modelo_orm.FuenteFinanciamiento.fuente == elem[17])
            
            try:
                modelo_orm.Obra.create(nombre=elem[0], monto_contrato=elem[4], fecha_inicio=elem[7], fecha_fin_inicial=elem[8], plazo_meses=elem[9], porcentaje_avance=elem[10], nro_contratacion=elem[13], mano_obra=elem[14], destacada=elem[15], nro_expediente=elem[16], etapa_id=etapa, tipo_obra_id=tipoObra, area_responsable_id=areaResp, comuna_id=comuna, barrio_id=barrio, empresa_id=empresa, tipo_contratacion_id=tipoContr, fuente_financiamiento_id=financiamiento)
            except IntegrityError as e:
                print(f'Error al insertar un nuevo registro en la tabla obra: {e}')
        
        sqlite_db.close()

    @classmethod
    def nueva_obra(cls):
        db = cls.conectar_db()

        modelo_orm.Obra.nuevo_proyecto()
        modelo_orm.Obra.iniciar_contratacion()
        modelo_orm.Obra.adjudicar_obra()
        modelo_orm.Obra.iniciar_obra()
        modelo_orm.Obra.actualizar_porcentaje_avance()

        while True:
            respuesta = input('Desea incrementar el plazo de meses que lleva la obra en ejecución? (SI/NO): ')
            if respuesta == 'SI':
                modelo_orm.Obra.incrementar_plazo()
                break
            elif respuesta == 'NO':
                break
            else:
                print('La respuesta no es valida.\nIngresar la respuesta nuevamente')

        while True:
            respuesta = input('Desea incrementar la mano de obra? (SI/NO): ')
            if respuesta == 'SI':
                modelo_orm.Obra.incrementar_mano_obra()
                break
            elif respuesta == 'NO':
                break
            else:
                print('La respuesta no es valida.\nIngresar la respuesta nuevamente')

        while True:
            respuesta = int(input('Desea:\n1. Finalizar la obra\n2. Rescindir la obra\n: '))
            if respuesta == 1:
                modelo_orm.Obra.finalizar_obra()
                break
            elif respuesta == 2:
                modelo_orm.Obra.rescindir_obra()
                break
            else:
                print('La respuesta no es valida.\nIngresar la respuesta nuevamente')

        sqlite_db.close()

    @classmethod
    def obtener_indicadores(cls):
        db = cls.conectar_db()

        print('\nAreas responsables:')
        for area in modelo_orm.AreaResponsable.select():
            print(area)

        ##############################################
        print('\nTipos de obra:')
        for tipo_obra in modelo_orm.TipoObra.select():
            print(tipo_obra)

        ##############################################
        print('\nCantidad de obras por etapa')
        for etapa in modelo_orm.Etapa.select():
            cantidad_obras = modelo_orm.Obra.select().where(modelo_orm.Obra.etapa == etapa).count()
            print(f"{etapa.estado}: {cantidad_obras} obras")

        ##############################################
        print('\nCantidad de obras y monto total de inversión por tipo de obra:')
        for tipo_obra in modelo_orm.TipoObra.select():
            monto_total = modelo_orm.Obra.select(fn.SUM(modelo_orm.Obra.monto_contrato)).where(modelo_orm.Obra.tipo_obra == tipo_obra).scalar()
            cantidad_obras = modelo_orm.Obra.select().where(modelo_orm.Obra.tipo_obra == tipo_obra).count()
            print(f"-{tipo_obra.tipo}: {cantidad_obras} obras, Monto total de inversión: {monto_total}")
        
        ##############################################
        print('\nListado de todos los barrios pertenecientes a las comunas 1, 2 y 3:')
        barrios_list = []
        for barrio in modelo_orm.Barrio.select():
            if modelo_orm.Comuna.get_by_id(barrio.comuna_id).numero <= 3:
                print(barrio.nombre)
        #print(barrios_list)
        
        ##############################################
        print('\nCantidad de obras finalizadas y su y monto total de inversión en la comuna 1:')
        obras_finalizadas_comuna1 = modelo_orm.Obra.select().where((modelo_orm.Obra.etapa == modelo_orm.Etapa.get(modelo_orm.Etapa.estado == 'Finalizada')) & (modelo_orm.Obra.comuna == modelo_orm.Comuna.get(modelo_orm.Comuna.numero == 1))).count()
        
        monto_total = modelo_orm.Obra.select(fn.SUM(modelo_orm.Obra.monto_contrato)).where((modelo_orm.Obra.etapa == modelo_orm.Etapa.get(modelo_orm.Etapa.estado == 'Finalizada')) & (modelo_orm.Obra.comuna == modelo_orm.Comuna.get(modelo_orm.Comuna.numero == 1))).scalar()
        
        print(f'Obras finalizadas en la comuna 1: {obras_finalizadas_comuna1}')
        print(f"Monto total de inversión en obras finalizadas de la comuna 1: {monto_total}")

        ##############################################
        print('\nCantidad de obras finalizadas en un plazo menor o igual a 24 meses:')
        obras_finalizadas_plazo = modelo_orm.Obra.select().where(modelo_orm.Obra.plazo_meses <= 24).count()
        print(obras_finalizadas_plazo)

        ##############################################
        print('\nPorcentaje de obras finalizadas:')
        total_obras = modelo_orm.Obra.select().count()
        obras_finalizadas = modelo_orm.Obra.select().where(modelo_orm.Obra.etapa == modelo_orm.Etapa.get(modelo_orm.Etapa.estado == 'Finalizada')).count()
        porcentaje_obras_finalizadas = (obras_finalizadas / total_obras) * 100 
        print('{:.2f}'.format(porcentaje_obras_finalizadas),"%")

        ##############################################
        print('\nCantidad total de mano de obra empleada:')
        cantidad_total = modelo_orm.Obra.select(fn.SUM(modelo_orm.Obra.mano_obra)).scalar()
        print(cantidad_total)

        ##############################################
        print('\nMonto total de inversión:')
        monto_total_inversion = modelo_orm.Obra.select(fn.SUM(modelo_orm.Obra.monto_contrato)).scalar()
        print(f"El monto total de inversion es de: {monto_total_inversion}")

        sqlite_db.close()

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