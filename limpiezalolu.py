import pandas as pd

df = pd.read_csv('https://cdn.buenosaires.gob.ar/datosabiertos/datasets/secretaria-general-y-relaciones-internacionales/ba-obras/observatorio-de-obras-urbanas.csv', sep=";", index_col=0, encoding='latin-1')

##print(df.isna().sum()) # cuantos valores faltan x columna (tipo -> 27 datos faltan)

# tipo - nombre - etapa - area_responsable

#tipo = df['tipo'].fillna('Indeterminado') # rellena el valor
#print (tipo.unique()) # de tipo único

# borrar repetidos, normalizar tablas, fk identificar

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