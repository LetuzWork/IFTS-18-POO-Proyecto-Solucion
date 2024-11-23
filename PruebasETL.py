import pandas as pd
from peewee import *
import random

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

# Normalizar los valores de la columna 'financiamiento'
dfmycols['financiamiento'] = dfmycols['financiamiento'].replace({
    'No especificado': 'No especificado',
    'Fuente 11': 'Nación / Fuente 11',
    'Fuente 14': 'Nación / Fuente 14',
    'FODUS': 'GCBA / FoDUS',
    'GCBA': 'GCBA',
    'F11': 'Nación / Fuente 11',
    'CAF-Nación-GCBA': 'Mixto / CAF / Nación / GCBA',
    'Nación-GCBA': 'Mixto / Nación / GCBA',
    'Préstamo BIRF 8706-AR': 'Mixto / Nación / Préstamo BIRF 8706-AR',
    'Préstamo BID AR-L1260': 'Mixto Nación / Préstamo BID AR-L1260',
    'PPI': 'Internacional',
})
exp = dfmycols['expediente-numero'].dropna().unique() # Extraer los valores únicos de la columna 'expediente-numero'
# Normalizar los valores de la columna 'expediente-numero'
dfmycols['expediente-numero'] = dfmycols.apply(
    lambda row: row['nro_contratacion'] if pd.isna(row['expediente-numero']) else row['expediente-numero'],
    axis=1
)
dfmycols['expediente-numero'] = dfmycols['expediente-numero'].str.replace(r'[/?.]', '-', regex=True)
print(exp)
print(dfmycols.head(15))

print(dfmycols['financiamiento'].unique())

# Obtener las fuentes de financiamiento únicas, excluyendo 'No especificado'
ffinanciamiento = dfmycols['financiamiento'].unique().tolist()
ffinanciamiento.remove('No especificado')

# Asignar de manera aleatoria una fuente de financiamiento a los valores 'No especificado'
dfmycols['financiamiento'] = dfmycols['financiamiento'].apply(
    lambda x: random.choice(ffinanciamiento) if x == 'No especificado' else x
)
# Asigno de manera aleatoria valores a la columna 'mano_obra' que sean diferentes de '0'
dfmycols['mano_obra'] = dfmycols['mano_obra'].apply(
    lambda x: random.randint(12, 79) if x == '0' else x
)
print(dfmycols.head())

# Combinar los valores limpios de dfmycols con dfOK
df_combined = dfOK.copy()
for column in dfmycols.columns:
    df_combined[column] = dfmycols[column]

    # Pasar valores únicos de financiamiento a una lista
    financiamiento_unicos = dfmycols['financiamiento'].unique().tolist()
    print(financiamiento_unicos)

for elem in financiamiento_unicos:
    print(elem)


df_combined.to_csv('camposdeinteresMech.csv', sep=';', encoding='latin-1')