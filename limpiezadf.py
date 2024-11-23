import pandas as pd

# Tarea limpiar los datos

df = pd.read_csv('https://cdn.buenosaires.gob.ar/datosabiertos/datasets/secretaria-general-y-relaciones-internacionales/ba-obras/observatorio-de-obras-urbanas.csv', sep=";", index_col=0, encoding='latin-1')

# 'descripcion' 'monto_contrato' 'comuna' 'barrio' 'direccion'

### 'descripcion', 'barrio', 'direccion' ###  Eliminados espacios inncesarios y convertidos todos a minusculas

df['descripcion'] = df['descripcion'].fillna('Indeterminado').str.strip().str.lower()

df['barrio'] = df['barrio'].fillna('Indeterminado').str.strip().str.lower()

df['direccion'] = df['direccion'].fillna('Indeterminado').str.strip().str.lower()

### monto_contrato ### 
df['monto_contrato'] = df['monto_contrato'].str.replace(r'[$.]', '', regex=True) #Reemplaza las signos '$' y '.' por vacios

df['monto_contrato'] = df['monto_contrato'].str.replace(r'(?<=\d),(?=\d{3})', '', regex=True, n=2) #Elimina las comas que son separadores de miles y elimina solo las 2 primeras coincidencias

df['monto_contrato'] = df['monto_contrato'].str.replace(',', '.') # Reemplaza las comas por puntos

df['monto_contrato'] = df['monto_contrato'].str.replace(r'\s*\(.*?\)', '', regex=True) # Borra los datos que estan entre parentesis

df['monto_contrato'] = df['monto_contrato'].fillna('0.00').str.strip().str.extract(r'[-+]?\$?([\d.,]+)').replace({',': ''}, regex=True).astype(float) # Extrae los primeros datos numericos de las oraciones y los convierte en datos validos


### comuna ### Convertido a numeros 
df['comuna'] = pd.to_numeric(df['comuna'], errors= 'coerce').fillna(0).astype(int)

