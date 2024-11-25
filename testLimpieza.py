import numpy as np
import pandas as pd

def obtener_unicos(df, columnas, nombre_columna_principal):
    """Obtiene los valores Unicos para normalizar tablas."""
    df_unicos = df[columnas].fillna('Indeterminado').drop_duplicates(subset=columnas[0]).reset_index(drop=True)

    if(nombre_columna_principal):
        df_unicos = df_unicos.rename(columns={columnas[0]: nombre_columna_principal})
    return df_unicos 

def limpiar_texto(df, columna):
    """ Elimina los espacios vacios y convierte a minuscula """
    df[columna] = df[columna].fillna('Indeterminado').str.strip().str.lower()
    return df

def limpiar_columnas(df):
    """Limpia las columnas del DataFrame."""
    
    # Limpiar las columnas de texto utilizando la nueva función
    columnas_texto = ['descripcion', 'barrio', 'direccion', 'mano_obra', 'expediente-numero', 'financiamiento']
    for col in columnas_texto:
        df = limpiar_texto(df, col)
    
    # Limpiar monto_contrato
    df['monto_contrato'] = df['monto_contrato'].str.replace(r'[$.]', '', regex=True)  # Reemplaza '$' y '.' por vacíos
    df['monto_contrato'] = df['monto_contrato'].str.replace(r'(?<=\d),(?=\d{3})', '', regex=True, n=2)  # Elimina comas como separador de miles
    df['monto_contrato'] = df['monto_contrato'].str.replace(',', '.')  # Reemplaza comas por puntos
    df['monto_contrato'] = df['monto_contrato'].str.replace(r'\s*\(.*?\)', '', regex=True)  # Elimina contenido entre paréntesis
    df['monto_contrato'] = df['monto_contrato'].fillna('0.00').str.strip().str.extract(r'[-+]?\$?([\d.,]+)').replace({',': ''}, regex=True).astype(float)  # Extrae valores numéricos

    # Limpiar comuna
    df['comuna'] = pd.to_numeric(df['comuna'], errors='coerce').fillna(0).astype(int)

    # Limpiar fecha_inicio y fecha_fin_inicial
    df['fecha_inicio'] = pd.to_datetime(df['fecha_inicio'], errors='coerce')
    df['fecha_fin_inicial'] = pd.to_datetime(df['fecha_fin_inicial'], errors='coerce')

    # Limpiar plazo_meses
    df['plazo_meses'] = pd.to_numeric(df['plazo_meses'], errors='coerce')
    df['plazo_meses'] = df['plazo_meses'].fillna(df['plazo_meses'].median()).astype(int)

    # Limpiar porcentaje_avance
    def limpiar_porcentaje(valor):
        if pd.isna(valor):
            return np.nan
        if isinstance(valor, (int, float)):
            return valor * 100 if valor <= 1 else valor
        if isinstance(valor, str):
            valor = valor.replace('%', '').strip()
            try:
                return float(valor)
            except ValueError:
                return np.nan
        return np.nan

    df['porcentaje_avance'] = df['porcentaje_avance'].apply(limpiar_porcentaje)
    df['porcentaje_avance'] = df['porcentaje_avance'].clip(0, 100)

    # Limpiar licitacion_oferta_empresa
    df['licitacion_oferta_empresa'] = df['licitacion_oferta_empresa'].str.strip()

    # Limpiar cuit_contratista
    df['cuit_contratista'] = df['cuit_contratista'].astype(str)
    df['cuit_contratista'] = df['cuit_contratista'].str.replace(r'[\n;]', ',', regex=True)
    df['cuit_contratista'] = df['cuit_contratista'].str.replace(r'[^0-9,]', '', regex=True)

    # Limpiar licitacion_anio
    df['licitacion_anio'] = df['licitacion_anio'].astype(str)
    df['licitacion_anio'] = df['licitacion_anio'].str.replace(r'[^0-9]', '', regex=True)

    # Limpiar contratacion_tipo
    df['contratacion_tipo'] = df['contratacion_tipo'].astype(str)
    df['contratacion_tipo'] = df['contratacion_tipo'].str.replace('-', '')  # Remover guiones

    return df

# Lista de columnas de interés
columnas_interes = [
    'tipo', 'nombre', 'etapa', 'area_responsable', 'descripcion', 
    'monto_contrato', 'barrio', 'comuna', 'direccion', 'fecha_inicio', 
    'fecha_fin_inicial', 'plazo_meses', 'porcentaje_avance', 
    'licitacion_oferta_empresa', 'cuit_contratista', 'licitacion_anio', 
    'contratacion_tipo', 'nro_contratacion', 'mano_obra', 'expediente-numero', 
    'financiamiento'
]

df = pd.read_csv('https://cdn.buenosaires.gob.ar/datosabiertos/datasets/secretaria-general-y-relaciones-internacionales/ba-obras/observatorio-de-obras-urbanas.csv', sep=";", index_col=0, encoding='latin-1').reset_index(drop=True)

# Aplicar la limpieza de datos
df_limpio = limpiar_columnas(df[columnas_interes])


def obtener_unicos_para_tablas_normalizadas():
    # Retornar las listas si es necesario
    return {
        'empresas': obtener_unicos(df_limpio,['licitacion_oferta_empresa', 'cuit_contratista'], 'nombre'),
        'barrios': obtener_unicos(df_limpio,['barrio','comuna'], 'nombre'),
        'tipos_contratacion': obtener_unicos(df_limpio,['contratacion_tipo'], 'nombre'),
        'fuentes_financiamiento': obtener_unicos(df_limpio,['financiamiento'], 'nombre'),
        'tipos_obra': obtener_unicos(df_limpio,['tipo'], 'nombre'),
        'areas_responsables': obtener_unicos(df_limpio, ['area_responsable'], 'nombre'),
        'etapas':  obtener_unicos(df_limpio,['etapa'], 'nombre')
    }

listas_unicas = obtener_unicos_para_tablas_normalizadas()
print(listas_unicas)
print(df_limpio.head())
