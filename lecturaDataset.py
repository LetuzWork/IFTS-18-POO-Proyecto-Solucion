import pandas as pd

df = pd.read_csv('https://cdn.buenosaires.gob.ar/datosabiertos/datasets/secretaria-general-y-relaciones-internacionales/ba-obras/observatorio-de-obras-urbanas.csv', sep=";", index_col=0, encoding='latin-1')

#print(df.columns[0:34])
#print(df.describe())

#dft = df.T

#print(dft)

dfnew = df.copy()
#print(f'luego de la copia: {dfnew}')

#dfnew = dfnew.fillna(value=5) #How=any (si hay un valor vacío para cuaquiera de las columnas, se rellena con 5)
dfnew = dfnew.dropna(axis=1, how='all') #How=all (si hay un valor vacío para todas las columnas, se elimina la fila)
#print(f'luego de dropna: {dfnew}')
#def leer_dataset(path): 
#   return pd.read_csv(path, sep=";", index_col=0, encoding='latin-1') #Solucion de encoding de Maxi para la lectura de bases de datos
#print(dfnew['barrio'].isnull().sum()) #Cantidad de valores nulos en la columna barrio
#print(dfnew['etapa'].isnull().sum()) #Cantidad de valores no nulos en la columna entorno

#print(dfnew['etapa'].value_counts()) #Cantidad de valores no nulos en la columna etapa

'''[OUT]
Finalizada                1471
En obra                     65
En ejecución                48
En licitación               21
Desestimada                 17
Rescisión                    7
Adjudicada                   7
Paralizada                   6
En armado de pliegos         6
En Ejecución                 4
Neutralizada                 3
Finalizada/desestimada       3
En Obra                      2
En proyecto                  2
En curso                     1
Proyecto finalizado          1
Anteproyecto                 1
Name: count, dtype: int64'''

#print(dfnew['area_responsable'].value_counts()) #Cantidad de valores no nulos en la columna area_responsable

'''[OUT]
area_responsable
Ministerio de Educación                           303
Ministerio de Espacio Público e Higiene Urbana    289
Corporación Buenos Aires Sur                      283
Secretarí­a de Transporte y Obras Públicas        235
Ministerio de Salud                               191
Ministerio de Desarrollo Humano y Hábitat         137
Subsecretarí­a de Gestión Comunal                  97
Instituto de la Vivienda                           40
Ministerio de Seguridad                            38
Subsecretaría de Proyectos y Obras                 24
Ministerio de Cultura                              20
Ministerio de Infraestructura                       8
Name: count, dtype: int64'''

#print(dfnew['monto_contrato']) #Cantidad de valores no nulos en la columna monto_contrato

'''[OUT]
entorno
Plan 54 escuelas                    $67.065.700,00
Donado Holmberg                      $9.950.017,00
Área Ambiental Central              $36.942.632,00
Área Ambiental Central              $26.938.294,00
Villa Olí­mpica                    $148.823.367,00
                                       ...
Registro Civil                     $297.828.720,70
Cementerios                        $864.892.138,20
Acumar                           $1.519.627.676,47
Acumar                             $126.012.191,03
Tribunal Superior de Justicia    $1.800.113.121,00
Name: monto_contrato, Length: 1665, dtype: object'''

