import sqlite3 as sql3
import pymysql
from peewee import *


conn = sql3.connect("database.db")
cursor = conn.cursor()

""" orm_db = SqliteDatabase('/Final-POO/obras_urbanas.db', pragmas={
    'journal_mode': 'wal'})

try:
    orm_db.connect()
except OperationalError as e:
    print("Se ha generado un error en la conexion a la BD.", e)
    exit()
    
     """


class BaseModel(Model):
    """El modelo base que usará nuestra base de datos Sqlite."""
    class Meta:
        #Este modelo ORM usa la base de datos "obras_urbanas.db".
        database = conn

class TipoObra(BaseModel):
    """Modelo de la tabla TipoObra."""
    id = IntegerField(primary_key=True)
    nombre = CharField(max_length=80)
    
    class Meta:
        #Nombre de la tabla. En plural
        table_name = 'tipoObras'

class AreaResponsable(BaseModel):
    """Modelo de la tabla AreaResponsable."""
    id = IntegerField(primary_key=True)
    nombre = CharField(max_length=80)
    
    class Meta:
        #Nombre de la tabla. En plural
        table_name = 'areaResponsable'

class Etapa(BaseModel):
    """Modelo de la tabla Etapa."""
    id = IntegerField(primary_key=True)
    nombre = CharField(max_length=80)
    
    class Meta:
        #Nombre de la tabla. En plural
        table_name = 'etapas'
        
class Obra(BaseModel): #Nombre de la clase en singular
    """Modelo de la tabla Obras."""
    id = IntegerField(primary_key=True)
    tipo_obra = ForeignKeyField(TipoObra, backref='tipoObras')
    area_responsable = ForeignKeyField(AreaResponsable, backref='areaResponsable')
    barrio = CharField(max_length=80)
    destacada = BooleanField()
    fecha_inicio = DateField()
    fecha_fin_inicial = DateField()
    porcentaje_avance = FloatField()
    plazo_meses = IntegerField()
    mano_obra = IntegerField()
    etapa = ForeignKeyField(Etapa, backref='etapas')
    
    
    class Meta:
        #Nombre de la tabla. En plural
        table_name = 'obras'

