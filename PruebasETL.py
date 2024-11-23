import pandas as pd
from peewee import *
import random

from modelo_orm import Barrio

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
#print(dfmechCols.head())

# Combinar los valores limpios de dfmechCols con dfOK
dfdieCols = dfOK[dieCols]
df_combined = dfOK.copy()

'''dfdieCols.dropna(how='all', inplace=True)

dfdieCols['descripcion'] = dfdieCols['descripcion'].fillna('Indeterminado').str.strip().str.lower()

dfdieCols['barrio'] = dfdieCols['barrio'].fillna('Indeterminado').str.strip().str.lower()

dfdieCols['direccion'] = dfdieCols['direccion'].fillna('Indeterminado').str.strip().str.lower()
'''
dfbarrio = dfdieCols['barrio'].unique()
dfcomuna = dfdieCols['comuna'].unique()

dfbarriocomuna = dfdieCols[['barrio', 'comuna']].dropna().drop_duplicates()
# Contar los valores únicos en cada columna
dfbarriocomuna = dfdieCols[['barrio', 'comuna']].dropna().drop_duplicates().groupby(['barrio', 'comuna']).size().reset_index(name='count')
print(dfbarriocomuna)

C0 = [{'comuna_num': 0}, {'barrios':['Múltiples barrios']}]
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

dfRari = pd.DataFrame(lsComunas, columns=['barrios', 'comuna_num'])
# Crear un DataFrame con las comunas y sus barrios correspondientes
comunas_data = []
for comuna in lsComunas:
    comuna_num = comuna[0]['comuna_num']
    barrios = comuna[1]['barrios']
    for barrio in barrios:
        comunas_data.append({'comuna': comuna_num, 'barrio': barrio})

df_comunas = pd.DataFrame(comunas_data)

# Normalizar los valores de la columna 'barrio' y 'comuna' en dfdieCols
dfdieCols['barrio'] = dfdieCols['barrio'].str.strip().str.lower()
dfdieCols['comuna'] = dfdieCols['comuna'].fillna(0)
# Reemplazar valores similares a "monsterrat" por "Montserrat"
lsBarrio = dfdieCols['barrio'].unique().tolist()
print(lsBarrio)

# Reemplazar los valores de la columna 'barrio' con sus correspondientes comunas
barrio_to_comuna = {
    'villa urquiza': 12, 'montserrat': 1, 'san nicolás': 1, 'villa lugano': 8, 'villa soldati': 8, 'puerto madero': 1, 'recoleta': 2, 'liniers': 9, 'villa riachuelo': 8, 'coghlan': 12, 'la boca': 4, 'belgrano': 13, 'parque patricios': 4, 'barracas': 4, 'palermo': 14, 'saavedra': 12, 'villa del parque': 11, 'almagro': 5, 'villa devoto': 11, 'villa pueyrredon': 12, 'agronomía': 15, 'san cristóbal': 3, 'balvanera': 3, 'flores': 7, 'villa luro': 10, 'chacarita': 15, 'parque avellaneda': 9, 'mataderos': 9, 'paternal': 15, 'caballito': 6, 'monte castro': 10, 'floresta': 10, 'parque chacabuco': 7, 'constitución': 1, 'nueva pompeya': 4, 'villa gral. mitre': 11, 'boedo': 5, 'nuñez': 13, 'constitucion': 1, 'villa crespo': 15, 'colegiales': 13, 'retiro': 1, 'san telmo': 1, 'vélez sarsfield': 10, 'villa real': 10, 'villa santa rita': 11, 'versalles': 10, 'parque chas': 15, 'villa 6 - barrio cildañez': 0, 'villa ortuzar': 15, 'nuã±ez': 13, 'villa ortúzar': 15, 'monserrat': 1, 'marcos paz': 0, 'san cristobal': 3, 'cuenca matanza- riachuelo': 0, 'barracas y nueva pompeya': 0, 'la boca y san telmo': 0, 'san nicolas': 1, 'lugano': 8, 'boca': 4, 'territorio caba': 0, 'recoleta, palermo y retiro': 0, 'san nicolas, monserrat, san telmo y la boca': 0, 'p. chacabuco/palermo': 0, 'p. chacabuco/agronomía/ palermo': 0, 'devoto': 11, 'flores, floresta': 0, 'mataderos, villa riachuelo, barracas, nueva pompeya, villa lugano y la boca': 0, '.': 0, 'velez sarsfield': 10, 'villa soldati, flores, floresta, parque avellaneda, mataderos, villa lugano, villa riachuelo, villa lugano': 0, 'villa lugano, parque avellaneda y flores': 0, 'villa soldati y saavedra': 0, 'villa soldati, flores, floresta, parque avellaneda, mataderos, villa lugano, villa riachuelo, villa lugano, liniers, parque chacabuco, caballito, boedo, san cristobal, constitución, boca, barracas, parque patricios  y nueva pompeya': 0, 'nuñez y saavedra': 0, 'yerbal - villa luro - velez sarfield floresta - monte castro - villa del parque - villa santa rita - paternal - villa crespo - villa urquiza': 0
}

dfdieCols['comuna'] = dfdieCols['barrio'].map(barrio_to_comuna).fillna(dfdieCols['comuna'])


# Verificar los cambios
print(dfdieCols[['barrio', 'comuna']].drop_duplicates())


       #dfbarriocomuna.loc[dfbarriocomuna['barrio'] == barrio, 'comuna'] = comuna_num

#dfbarriocomuna.to_csv('barrioComuna.csv', sep=';', encoding='latin-1')

# 48 barrios en total
# 15 comunas en total

### monto_contrato ### 
'''dfdieCols['monto_contrato'] = dfdieCols['monto_contrato'].str.replace(r'[$.]', '', regex=True) #Reemplaza las signos '$' y '.' por vacios

dfdieCols['monto_contrato'] = dfdieCols['monto_contrato'].str.replace(r'(?<=\d),(?=\d{3})', '', regex=True, n=2) #Elimina las comas que son separadores de miles y elimina solo las 2 primeras coincidencias

dfdieCols['monto_contrato'] = dfdieCols['monto_contrato'].str.replace(',', '.') # Reemplaza las comas por puntos

dfdieCols['monto_contrato'] = dfdieCols['monto_contrato'].str.replace(r'\s*\(.*?\)', '', regex=True) # Borra los datos que estan entre parentesis
'''
#dfdieCols['monto_contrato'] = dfdieCols['monto_contrato'].fillna('0.00').str.strip().str.extract(r'[-+]?\$?([\d.,]+)').replace({',': ''}, regex=True).astype(float) # Extrae los primeros datos numericos de las oraciones y los convierte en datos validos

#Se podrá hacer en una línea:
#dfdieCols['monto_contrato'] = dfdieCols['monto_contrato'].str.replace(r'[$.]', '', regex=True).str.replace(r'(?<=\d),(?=\d{3})', '', regex=True, n=2).str.replace(',', '.').str.replace(r'\s*\(.*?\)', '', regex=True).fillna('0.00').str.strip().str.extract(r'[-+]?\$?([\d.,]+)').replace({',': ''}, regex=True).astype(float)

### comuna ### Convertido a numeros 
#dfdieCols['comuna'] = pd.to_numeric(dfdieCols['comuna'], errors= 'coerce').fillna(0).astype(int)

#for column in dfdieCols.columns:
#    unique_values = dfdieCols[column].unique()
    #print(f"Los valores unicos de la columna : '{column}': {unique_values}")

#dfdieCols = dfdieCols.fillna({'comuna': 'No especificado', 'barrio': 'No especificado', 'direccion': 'No especificado'})
#for column in dfmechCols.columns:
#    df_combined[column] = dfmechCols[column]

#for column in dfdieCols.columns:
#    df_combined[column] = dfdieCols[column]

#df_combined.to_csv('camposdeinteresMechDie.csv', sep=';', encoding='latin-1')

#df_combined.to_csv('camposdeinteresMech.csv', sep=';', encoding='latin-1')

