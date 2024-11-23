from peewee import *
from datetime import timedelta

db = SqliteDatabase('obras_urbanas.db', pragmas ={'journal_mode' : 'wal'})

""" orm_db = SqliteDatabase('/Final-POO/obras_urbanas.db', pragmas={
    'journal_mode': 'wal'}) #Si existe se conecta a la bbdd y sino crea la conexion (el archivo) string de conexión
    orm_db.connect() #se crea la instancia de conexion """

class BaseModel(Model):
    """El modelo base que usará nuestra base de datos Sqlite."""
    class Meta:
        #Este modelo ORM usa la base de datos "obras_urbanas.db"
        database = db

class Empresa(BaseModel):
    id = AutoField()
    nombre = CharField(max_length=100)
    cuit = CharField(max_length=20, unique=True)

    class Meta:
        #Nombre de la tabla. En plural
        table_name = 'empresas'

class Barrio(BaseModel):
    id = AutoField()
    nombre = CharField(max_length=100)
    comuna = IntegerField(null=True)

    class Meta:
        #Nombre de la tabla. En plural
        table_name = 'barrios'

class TipoContratacion(BaseModel):
    id = AutoField()
    nombre = CharField(max_length=100)

    class Meta:
        #Nombre de la tabla. En plural
        table_name = 'tipos_contratacion'

class FuenteFinanciamiento(BaseModel):
    id = AutoField()
    nombre = CharField(max_length=100)

    class Meta:
        #Nombre de la tabla. En plural
        table_name = 'fuentes_financiamiento'

class TipoObra(BaseModel):
    """Modelo de la tabla TipoObra."""
    id = AutoField()
    nombre = CharField(max_length=80)
    
    class Meta:
        #Nombre de la tabla. En plural
        table_name = 'tipo_obras'

class AreaResponsable(BaseModel):
    """Modelo de la tabla AreaResponsable."""
    id = AutoField()
    nombre = CharField(max_length=80)
    
    class Meta:
        #Nombre de la tabla. En plural
        table_name = 'areas_responsables'

class Etapa(BaseModel):
    """Modelo de la tabla Etapa."""
    id = AutoField()
    nombre = CharField(max_length=80)
    
    class Meta:
        #Nombre de la tabla. En plural
        table_name = 'etapas'

class Obra(BaseModel):
    """Modelo de la tabla Obras."""
    id = AutoField()
    tipo_obra = ForeignKeyField(TipoObra, backref='obras')
    area_responsable = ForeignKeyField(AreaResponsable, backref='obras')
    barrio = ForeignKeyField(Barrio, backref='obras')
    destacada = BooleanField()
    fecha_inicio = DateField(null=True)
    fecha_fin_inicial = DateField(null=True)
    porcentaje_avance = FloatField(null=True)
    plazo_meses = IntegerField(null=True)
    mano_obra = IntegerField(null=True)
    etapa = ForeignKeyField(Etapa, backref='obras')
    tipo_contratacion = ForeignKeyField(TipoContratacion, backref='obras', null=True)
    nro_contratacion = CharField(max_length=80, null=True)
    empresa = ForeignKeyField(Empresa, backref='obras', null=True)
    expediente_numero = CharField(max_length=80, null=True)
    fuente_financiamiento = ForeignKeyField(FuenteFinanciamiento, backref='obras', null=True)
    
    class Meta:
        #Nombre de la tabla. En plural
        table_name = 'obras'

    def nuevo_proyecto(self, tipo_obra, area_responsable, barrio):
        self.etapa, _ = Etapa.get_or_create(nombre="Proyecto")
        self.tipo_obra = tipo_obra
        self.area_responsable = area_responsable
        self.barrio = barrio

        self.save()

    def iniciar_contratacion(self, tipo_contratacion, nro_contratacion):
        self.tipo_contratacion = tipo_contratacion
        self.nro_contratacion = nro_contratacion
        self.save()

    def adjudicar_obra(self, empresa, nro_expediente):
        self.empresa = empresa
        self.expediente_numero = nro_expediente
        self.save()

    def iniciar_obra(self, destacada, fecha_inicio, fecha_fin_inicial, fuente_financiamiento, mano_obra):
        self.destacada = destacada
        self.fecha_inicio = fecha_inicio
        self.fecha_fin_inicial = fecha_fin_inicial
        self.fuente_financiamiento = fuente_financiamiento
        self.mano_obra = mano_obra
        self.etapa, _ = Etapa.get_or_create(nombre="En Ejecución")
        self.save()

    def actualizar_porcentaje_avance(self, porcentaje):
        if 0 <= porcentaje <= 100:
            self.porcentaje_avance = porcentaje
            self.save()
        else:
            raise ValueError("El porcentaje debe estar entre 0 y 100.")
    
    def incrementar_plazo(self, meses):
        if not isinstance(meses, int) or meses < 0:
            raise ValueError("El incremento debe ser un número entero positivo.")

        if self.plazo_meses is None:
            self.plazo_meses = meses
        else:
            self.plazo_meses += meses

        if self.fecha_fin_inicial:
            # Aproximación de meses a días utilizando timedelta
            self.fecha_fin_inicial += timedelta(days=meses * 30)

        self.save()
        return f"Plazo incrementado en {meses} meses. Nuevo plazo total: {self.plazo_meses} meses."


    def incrementar_mano_obra(self, cantidad):
        if cantidad > 0:
            self.mano_obra += cantidad
            self.save()
        else:
            raise ValueError("La cantidad debe ser positiva.")

    def finalizar_obra(self):
        self.etapa, _ = Etapa.get_or_create(nombre='Finalizada')
        self.porcentaje_avance = 100
        self.save()

    def rescindir_obra(self):
        self.etapa, _ = Etapa.get_or_create(nombre='Rescindida')
        self.save()

def create_tables():
    with db:
        db.create_tables([Empresa, Barrio, TipoContratacion, FuenteFinanciamiento, TipoObra, AreaResponsable, Etapa, Obra])

if __name__ == '__main__':
    create_tables()
    print("Tablas creadas exitosamente.")

# orm_db.commit()

#return pd.read_csv(path, sep=";", index_col=0, encoding='latin-1') Solucion de encoding de Maxi para la lectura de bases de datos