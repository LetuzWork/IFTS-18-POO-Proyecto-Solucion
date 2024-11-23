import numpy as np
import pandas as pd

df = pd.read_csv('https://cdn.buenosaires.gob.ar/datosabiertos/datasets/secretaria-general-y-relaciones-internacionales/ba-obras/observatorio-de-obras-urbanas.csv', sep=";", index_col=0, encoding='latin-1')
print (df.columns)

'''ar = df['area_responsable'].unique()
for x in ar:
        print(f"{x}") '''
        
'''[OUT]
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
Ministerio de Infraestructura'''

'''ti = df['cuit_contratista'].unique()
for x in ti:
        print(f"{x}") '''
'''[OUT] Entorno'''


list = ['tipo','nombre', 'etapa', 'area_responsable', 'descripcion',
       'monto_contrato', 'barrio','comuna', 'direccion','fecha_inicio', 'fecha_fin_inicial', 'plazo_meses', 'porcentaje_avance','licitacion_oferta_empresa', 'cuit_contratista', 'licitacion_anio', 'contratacion_tipo', 'nro_contratacion','mano_obra','expediente-numero','financiamiento',
       'nro_contratacion']
#print(len(list))

dftrim = df[list]
cuitNO = dftrim.dropna(subset = ['cuit_contratista'])
#print(cuitNO)
#print(dftrim.head())
#dftrim.to_csv('obras.csv', sep=';', encoding='latin-1')

##fin = dftrim['financiamiento'].unique()
#for x in fin:
#        print(f"{x}")

#dftrim = dftrim.fillna({'mano_obra': np.random.choice(['354534', '345345', '5345'])})
dftrim = dftrim.fillna({'mano_obra': '0'})
#print(dftrim['mano_obra'].head(25))

#print(dftrim['porcentaje_avance'].unique())
#dftrim = dftrim.fillna({'porcentaje_avance':0})
#df[' '] = np.random.choice([' ', ' ', ' '], len(df)) 
print(dftrim.head(15))

'''for elem in dftrim.values:
        print(elem)'''

'''['Arquitectura'
 'Demolición por riesgo estructural Diógenes Taborda N° 1553' 'Adjudicada'
 'Subsecretaría de Proyectos y Obras'
 'Demolición de edificio con riesgo estructural' '$126.012.191,03'
 'Nueva Pompeya' '4' 'Diógenes Taborda N° 1553' 'A/D' 'A/D' '3' '0'
 'DEMOLICIONES MITRE' '30657536551' '2024' 'Contratación Directa'
 '10241-0001-CDI24' '5345' 'EX-2024-16633639-   -GCABA-DGTALMI' nan
 '10241-0001-CDI24']'''

tk = ['nombre', 'descripcion', 'imagen_1']
dftk = df[tk]
dftk = dftk.dropna(subset = [tk[1]])
dftk = dftk.dropna(subset = [tk[2]])
print(dftk)

