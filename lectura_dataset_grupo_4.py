import pandas as pd

df = pd.read_csv('https://cdn.buenosaires.gob.ar/datosabiertos/datasets/secretaria-general-y-relaciones-internacionales/ba-obras/observatorio-de-obras-urbanas.csv', sep=";", index_col=0, encoding='latin-1')

# Este Archivo es provisional y será mergeado con los demas grupos
# El Grupo 4 serian "licitacion_oferta_empresa", "cuit_contratista", "licitacion_anio", "contratacion_tipo","nro_contratacion"

##### licitacion_oferta_empresa #####
df["licitacion_oferta_empresa"] = df["licitacion_oferta_empresa"].str.strip()

# data para poblar tablas
empresas = df["licitacion_oferta_empresa"].dropna().unique()

##### cuit_contratista #####

df["cuit_contratista"] = df["cuit_contratista"].astype(str)
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

df["contratacion_tipo"] = df["contratacion_tipo"].str.replace(r'[-]', '', regex=True)

##### nro_contratacion #####
# Es un numero unico por obra pero con formato que varia entre obras, inicialmente sin formatear






