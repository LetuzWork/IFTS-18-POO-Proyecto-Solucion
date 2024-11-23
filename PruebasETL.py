import pandas as pd
from peewee import *

'''df = pd.read_csv('https://cdn.buenosaires.gob.ar/datosabiertos/datasets/secretaria-general-y-relaciones-internacionales/ba-obras/observatorio-de-obras-urbanas.csv', sep=";", index_col=0, encoding='latin-1')

camposdeInteres = ['nombre', 'etapa', 'tipo', 'area_responsable', 'descripcion',
       'monto_contrato', 'comuna', 'barrio', 'direccion', 'fecha_inicio', 'fecha_fin_inicial', 'plazo_meses', 'porcentaje_avance',
       'licitacion_oferta_empresa', 'licitacion_anio', 'contratacion_tipo',
       'nro_contratacion', 'cuit_contratista', 
      'expediente-numero', 'financiamiento']  # Replace with your actual column names
df = df[camposdeInteres]

print(df.head())
df.to_csv('camposdeinteres.csv', sep=';', encoding='latin-1')'''

dfOK = pd.read_csv('camposdeinteres.csv', sep=';', index_col=0, encoding='latin-1')
mycols = ['nro_contratacion', 'expediente-numero', 'financiamiento','mano_obra']

dfmycols = dfOK[mycols]
dfOK[mycols].dropna(how='all', inplace=True)

for column in dfmycols.columns:
    unique_values = dfOK[column].unique()
    print(f"Los valores unicos de la columna : '{column}': {unique_values}")

dfmycols = dfmycols.fillna({'financiamiento': 'No especificado', 'mano_obra': '0'})


print(dfmycols.head(), dfmycols.shape)

