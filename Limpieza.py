'''import numpy as np
import pandas as pd
from PruebasETL import df_combined

df = pd.read_csv('https://cdn.buenosaires.gob.ar/datosabiertos/datasets/secretaria-general-y-relaciones-internacionales/ba-obras/observatorio-de-obras-urbanas.csv', sep=";", index_col=0, encoding='latin-1')
print (df.columns)

ar = df['area_responsable'].unique()
for x in ar:
        print(f"{x}") 
        
[OUT]
Ministerio de Educación
Secretarí­a de Transporte y Obras Públicas
Corporación Buenos Aires Sur
Instituto de la Vivienda
Ministerio de Salud
Subsecretarí­a de Gestión Comunal
Ministerio de Cultura
Ministerio de Espacio Público e Higiene Urbana
Ministerio de Desarrollo Humano y Hábitat
Subsecretaría de Proyectos y Obras
Ministerio de Seguridad
Ministerio de Infraestructura

ti = df['cuit_contratista'].unique()
for x in ti:
        print(f"{x}") 
[OUT] Entorno


list = ['tipo','nombre', 'etapa', 'area_responsable', 'descripcion',
       'monto_contrato', 'barrio','comuna', 'direccion','fecha_inicio', 'fecha_fin_inicial', 'plazo_meses', 'porcentaje_avance','licitacion_oferta_empresa', 'cuit_contratista', 'licitacion_anio', 'contratacion_tipo', 'nro_contratacion','mano_obra','expediente-numero','financiamiento',
       'nro_contratacion']
#print(len(list))

df = df[list] # selecciono las columnas que me interesan

tk = ['nombre', 'descripcion', 'imagen_1']
dftk = df[tk]
dftk = dftk.dropna(subset = [tk[1]])
dftk = dftk.dropna(subset = [tk[2]])
print(dftk)

import pandas as pd

df = pd.read_csv('https://cdn.buenosaires.gob.ar/datosabiertos/datasets/secretaria-general-y-relaciones-internacionales/ba-obras/observatorio-de-obras-urbanas.csv', sep=";", index_col=0, encoding='latin-1')

# Este Archivo es provisional y será mergeado con los demas grupos
# Limpieza de Lolu
# Tipo
tipos = df[['tipo']].fillna('Indeterminado').drop_duplicates().reset_index(drop=True)
tipos['Tipo_ID'] = tipos.index + 1

print("Tabla de Tipos:")
print(tipos)

# Etapa
etapas = df[['etapa']].drop_duplicates().reset_index(drop=True)
etapas['Etapa_ID'] = etapas.index + 1

print("Tabla de Etapas:")
print(etapas)

# Área 
areas = df[['area_responsable']].drop_duplicates().reset_index(drop=True)
areas['Area_ID'] = areas.index + 1

print("Tabla de Áreas Responsables:")
print(areas)

# asocio ID d c/u en la tabla principal
df = df.merge(tipos, on='tipo')
df = df.merge(etapas, on='etapa')
df = df.merge(areas, on='area_responsable')

# tabla principal
obras = df[['nombre', 'Tipo_ID', 'Etapa_ID', 'Area_ID']]

print("Tabla Principal (Obras):")
print(obras)

tipos.to_csv("tipos.csv", index=False) # tabla con tipo de obra y el id
etapas.to_csv("etapas.csv", index=False) # tabla con etapa de la obra
areas.to_csv("areas_responsables.csv", index=False) # tabla con el area
obras.to_csv("obras.csv", index=False) # tabla principal que une nombres de las obras y id del tipo, etapa y área

print("Tablas normalizadas.")

import pandas as pd

df = pd.read_csv('https://cdn.buenosaires.gob.ar/datosabiertos/datasets/secretaria-general-y-relaciones-internacionales/ba-obras/observatorio-de-obras-urbanas.csv', sep=";", index_col=0, encoding='latin-1')

# Este Archivo es provisional y será mergeado con los demas grupos
# El Grupo 4 serian "licitacion_oferta_empresa", "cuit_contratista", "licitacion_anio", "contratacion_tipo","nro_contratacion"
##LIMPIEZA MARTO
##### licitacion_oferta_empresa #####
df["licitacion_oferta_empresa"] = df["licitacion_oferta_empresa"].str.strip() # Removiendo espacios en blanco al principio y al final

# data para poblar tablas
empresas = df["licitacion_oferta_empresa"].dropna().unique() # Empresas unicas

##### cuit_contratista #####

df["cuit_contratista"] = df["cuit_contratista"].astype(str) # Convirtiendo a string
# Estandarizando el separador
df["cuit_contratista"] = df["cuit_contratista"].str.replace(r'[\n;]', ',', regex=True) 
# Removiendo cualquier no numero excepto comas
df["cuit_contratista"] = df["cuit_contratista"].str.replace(r'[^0-9,]', '', regex=True)

##### licitacion_anio #####
df["licitacion_anio"] = df["licitacion_anio"].astype(str)
# Removiendo cualquier no numero
df["licitacion_anio"] = df["licitacion_anio"].str.replace(r'[^0-9]', '', regex=True)

##### contratacion_tipo #####
df["contratacion_tipo"] = df["contratacion_tipo"].astype(str)

#df["contratacion_tipo"] = df["contratacion_tipo"].str.replace(r'[-]', '', regex=True)
df["contratacion_tipo"] = df["contratacion_tipo"].str.replace('-', '') # Removiendo guiones sin Regex

##### nro_contratacion #####
# Es un numero unico por obra pero con formato que varia entre obras, inicialmente sin formatear


#AGREGO LIMPIEZA DIEGO:
# 'descripcion' 'monto_contrato' 'comuna' 'barrio' 'direccion'

### 'descripcion', 'barrio', 'direccion' ###  Eliminados espacios inncesarios y convertidos todos a minusculas

dfdieCols['descripcion'] = dfdieCols['descripcion'].fillna('Indeterminado').str.strip().str.lower()

dfdieCols['barrio'] = dfdieCols['barrio'].fillna('Indeterminado').str.strip().str.lower()

dfdieCols['direccion'] = dfdieCols['direccion'].fillna('Indeterminado').str.strip().str.lower()

### monto_contrato ### 
dfdieCols['monto_contrato'] = dfdieCols['monto_contrato'].str.replace(r'[$.]', '', regex=True) #Reemplaza las signos '$' y '.' por vacios

dfdieCols['monto_contrato'] = dfdieCols['monto_contrato'].str.replace(r'(?<=\d),(?=\d{3})', '', regex=True, n=2) #Elimina las comas que son separadores de miles y elimina solo las 2 primeras coincidencias

dfdieCols['monto_contrato'] = dfdieCols['monto_contrato'].str.replace(',', '.') # Reemplaza las comas por puntos

dfdieCols['monto_contrato'] = dfdieCols['monto_contrato'].str.replace(r'\s*\(.*?\)', '', regex=True) # Borra los datos que estan entre parentesis

dfdieCols['monto_contrato'] = dfdieCols['monto_contrato'].fillna('0.00').str.strip().str.extract(r'[-+]?\$?([\d.,]+)').replace({',': ''}, regex=True).astype(float) # Extrae los primeros datos numericos de las oraciones y los convierte en datos validos


### comuna ### Convertido a numeros 
dfdieCols['comuna'] = pd.to_numeric(dfdieCols['comuna'], errors= 'coerce').fillna(0).astype(int)

'''