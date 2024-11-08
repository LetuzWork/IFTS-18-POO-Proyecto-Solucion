from peewee import *
from datetime import datetime

sqlite_db = SqliteDatabase('./clase11/store.db', pragmas={'journal_mode': 'wal'})
#sqlite_db = MySQLDatabase('peewee_orm', user='root', password='', host='localhost', port=3306)

try:
    sqlite_db.connect()
except OperationalError as e:
    print("Se ha generado un error en la conexion a la BD.", e)
    exit()

class BaseModel(Model):
    """El modelo base que usará nuestra base de datos Sqlite."""
    class Meta:
        #Este modelo ORM usa la base de datos "store.db".
        database = sqlite_db

class Category(BaseModel):
    name = CharField(unique=True)

    def str(self):
        return self.name

    class Meta:
        db_table = 'categories'

class Product(BaseModel):
    name = CharField(max_length=80, unique=True)
    price = DoubleField()
    category = ForeignKeyField(Category, backref='products')

    def str(self):
        return self.name

    class Meta:
        db_table = 'products'

class Sale(BaseModel):
    date = DateTimeField(default=datetime.now)
    product = ForeignKeyField(Product, backref='sales')
    quantity = IntegerField()

    @property
    def total(self):
        return self.product.price * self.quantity

    def str(self):
        return self.date.strftime("%d/%m/%Y") + " - " + self.product.name + " - Cant:" + str(self.quantity) + " - Total: $ " + str(self.total)

    class Meta:
        db_table = 'sales'

#Creamos las tablas correspondientes a las clases del modelo "Category", "Product" y "Sale"
try:
    sqlite_db.create_tables([Category, Product, Sale])
    print("Se han creado correctamente las tablas de la BD.")
except OperationalError as e:
    print("Se ha generado un error al crear las tablas de la BD.")
    exit()