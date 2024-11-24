import pandas as pd
from peewee import *
import random
from fuzzywuzzy import process 


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
mechCols = ['nro_contratacion', 'expediente-numero', 'financiamiento','mano_obra']
dieCols = ['descripcion', 'monto_contrato', 'comuna', 'barrio', 'direccion']

dfmechCols = dfOK[mechCols]
dfOK[mechCols].dropna(how='all', inplace=True)

for column in dfmechCols.columns:
    unique_values = dfOK[column].unique()
    #print(f"Los valores unicos de la columna : '{column}': {unique_values}")

dfmechCols = dfmechCols.fillna({'financiamiento': 'No especificado', 'mano_obra': '0'})

# Normalizar los valores de la columna 'financiamiento'
dfmechCols['financiamiento'] = dfmechCols['financiamiento'].replace({
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
exp = dfmechCols['expediente-numero'].dropna().unique() # Extraer los valores únicos de la columna 'expediente-numero'
# Normalizar los valores de la columna 'expediente-numero'
dfmechCols['expediente-numero'] = dfmechCols.apply(
    lambda row: row['nro_contratacion'] if pd.isna(row['expediente-numero']) else row['expediente-numero'],
    axis=1
)
dfmechCols['expediente-numero'] = dfmechCols['expediente-numero'].str.replace(r'[/?.]', '-', regex=True)
#print(exp)
#print(dfmechCols.head(15))

#print(dfmechCols['financiamiento'].unique())

# Obtener las fuentes de financiamiento únicas, excluyendo 'No especificado'
ffinanciamiento = dfmechCols['financiamiento'].unique().tolist()
ffinanciamiento.remove('No especificado')

# Asignar de manera aleatoria una fuente de financiamiento a los valores 'No especificado'
dfmechCols['financiamiento'] = dfmechCols['financiamiento'].apply(
    lambda x: random.choice(ffinanciamiento) if x == 'No especificado' else x
)
# Asigno de manera aleatoria valores a la columna 'mano_obra' que sean diferentes de '0'
dfmechCols['mano_obra'] = dfmechCols['mano_obra'].apply(
    lambda x: random.randint(12, 79) if x == '0' else x
)
# Combinar los valores limpios de dfmechCols con dfOK
dfdieCols = dfOK[dieCols]
df_combined = dfOK.copy()

dfdieCols['barrio'].fillna('Múltiples Barrios', inplace=True)
dfbarrio = dfdieCols['barrio'].unique()
dfcomuna = dfdieCols['comuna'].unique()

dfbarriocomuna = dfdieCols[['barrio', 'comuna']].dropna().drop_duplicates()
# Contar los valores únicos en cada columna
dfbarriocomuna = dfdieCols[['barrio', 'comuna']].dropna().drop_duplicates().groupby(['barrio', 'comuna']).size().reset_index(name='count')
#print(dfbarriocomuna)

C0 = [{'comuna_num': 0}, {'barrios':['Múltiples Barrios']}]
C1 = [{'comuna_num': 1}, {'barrios': ['Retiro', 'San Nicolás', 'Puerto Madero', 'San Telmo', 'Montserrat', 'Constitución']}]
C2 = [{'comuna_num': 2}, {'barrios': ['Recoleta']}]
C3 = [{'comuna_num': 3}, {'barrios': ['Balvanera', 'San Cristóbal']}]
C4 = [{'comuna_num': 4}, {'barrios': ['La Boca', 'Barracas', 'Parque Patricios', 'Nueva Pompeya']}]
C5 = [{'comuna_num': 5}, {'barrios': ['Almagro', 'Boedo']}]
C6 = [{'comuna_num': 6}, {'barrios': ['Caballito']}]
C7 = [{'comuna_num': 7}, {'barrios': ['Flores', 'Parque Chacabuco']}]
C8 = [{'comuna_num': 8}, {'barrios': ['Villa Soldati', 'Villa Riachuelo', 'Villa Lugano']}]
C9 = [{'comuna_num': 9}, {'barrios': ['Liniers', 'Mataderos', 'Parque Avellaneda']}]
C10 = [{'comuna_num': 10}, {'barrios': ['Villa Real', 'Monte Castro', 'Versalles', 'Floresta', 'Vélez Sarfield', 'Villa Luro']}]
C11 = [{'comuna_num': 11}, {'barrios': ['Villa General Mitre', 'Villa Devoto', 'Villa del Parque', 'Villa Santa Rita']}]
C12 = [{'comuna_num': 12}, {'barrios': ['Coghlan', 'Saavedra', 'Villa Urquiza', 'Villa Pueyrredón']}]
C13 = [{'comuna_num': 13}, {'barrios': ['Núñez', 'Belgrano', 'Colegiales']}]
C14 = [{'comuna_num': 14}, {'barrios': ['Palermo']}]
C15 = [{'comuna_num': 15}, {'barrios': ['Chacarita', 'Villa Crespo', 'La Paternal', 'Villa Ortúzar', 'Agronomía', 'Parque Chas']}]

lsComunas = [C0, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14, C15]
# Crear una lista de todos los barrios dentro de lsComunas, sin importar las comunas
all_barrios = []
for comuna in lsComunas:
    barrios = comuna[1]['barrios']
    all_barrios.extend(barrios)

dfdieCols['barrio'] = dfdieCols['barrio'].str.replace('/', ',') # Reemplaza las comas por puntos
dfdieCols['barrio'] = dfdieCols['barrio'].str.replace('-', ',') # Reemplaza las comas por puntos

barriols = dfdieCols['barrio'].unique().tolist()

for barrio in barriols:
    b, percent = process.extractOne(barrio, all_barrios)
    x = b if percent > 85 else "Múltiples Barrios"
    #print (f"{barrio} -> {x} ({percent}%)")
    dfdieCols['barrio'] = dfdieCols['barrio'].replace(barrio, x)

dfdieCols['barrio'] = dfdieCols['barrio'].replace({'NuÃ±ez': 'Núñez',
                                                    'Agronomí\xada': 'Agronomía',
                                                    'San Nicolas': 'San Nicolás'
                                                     })



# Asignar de manera aleatoria un barrio a los valores cuyo dfdieCols['barrio2'].value_counts() sea 1:
regcount = dfdieCols['barrio'].value_counts()
regval = regcount[regcount == 1].index.tolist()

dfdieCols['barrio2'] = dfdieCols['barrio'].apply(
    lambda x: random.choice(all_barrios) if x in regval else x
)
dfdieCols['barrio'] = dfdieCols['barrio2']

comunas_data = []
for comuna in lsComunas:
    comuna_num = comuna[0]['comuna_num']
    barrios = comuna[1]['barrios']
    for barrio in barrios:
        comunas_data.append({'comuna': comuna_num, 'barrio': barrio})

# Crear un diccionario para mapear barrios a comunas
barrio_to_comuna = {item['barrio']: item['comuna'] for item in comunas_data}

# Reemplazar los valores de 'comuna' en dfdieCols con el número de comuna correspondiente
dfdieCols['comuna'] = dfdieCols['barrio'].map(barrio_to_comuna).fillna(0)

print(dfdieCols[['barrio', 'comuna']])
#print(sorted(dfdieCols['barrio'].unique()))
#print(dfdieCols['barrio'].value_counts())

dfbarriocomuna.to_csv('barrioComuna.csv', sep=';', encoding='latin-1')

# 48 barrios en total
# 15 comunas en total

for column in dfmechCols.columns:
    df_combined[column] = dfmechCols[column]

for column in dfdieCols.columns:
    df_combined[column] = dfdieCols[column]




df_combined.to_csv('camposdeinteresMechNormal.csv', sep=';', encoding='latin-1')

#df_combined.to_csv('camposdeinteresMech.csv', sep=';', encoding='latin-1')

