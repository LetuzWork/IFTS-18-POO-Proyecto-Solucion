import pandas as pd

df = pd.read_csv('https://cdn.buenosaires.gob.ar/datosabiertos/datasets/secretaria-general-y-relaciones-internacionales/ba-obras/observatorio-de-obras-urbanas.csv', sep=";", index_col=0, encoding='latin-1')

#print(df.columns[0:34])
print(df.describe())

dft = df.T

#print(dft)

dfnew = df.copy()
print(f'luego de la copia: {dfnew}')

#dfnew = dfnew.fillna(value=5)
dfnew = dfnew.dropna(axis=1, how='all')
print(f'luego de fillna: {dfnew}')
#def leer_dataset(path): 
 #   return pd.read_csv(path, sep=";", index_col=0, encoding='latin-1') #Solucion de encoding de Maxi para la lectura de bases de datos