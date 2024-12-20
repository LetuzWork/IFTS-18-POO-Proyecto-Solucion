import numpy as np
import pandas as pd

def limpiar_texto(df, columna):
    """Elimina los espacios vacíos y convierte a minúsculas."""
    df.loc[:, columna] = df[columna].fillna('Indeterminado').str.strip().str.lower()
    return df

def limpiar_columnas(df):
    """Limpia las columnas del DataFrame."""

    # Limpiar las columnas de texto utilizando la nueva función
    columnas_texto = ['descripcion', 'barrio', 'mano_obra', 'expediente-numero', 'financiamiento']
    for col in columnas_texto:
        df = limpiar_texto(df, col)
    
    # Limpiar monto_contrato
    df.loc[:, 'monto_contrato'] = df['monto_contrato'].str.replace(r'[$.]', '', regex=True)  # Reemplaza '$' y '.'
    df.loc[:, 'monto_contrato'] = df['monto_contrato'].str.replace(r'(?<=\d),(?=\d{3})', '', regex=True, n=2)  # Elimina comas como separadores de miles
    df.loc[:, 'monto_contrato'] = df['monto_contrato'].str.replace(',', '.')  # Reemplaza comas por puntos
    df.loc[:, 'monto_contrato'] = df['monto_contrato'].str.replace(r'\s*\(.*?\)', '', regex=True)  # Elimina contenido entre paréntesis

    df.loc[:, 'monto_contrato'] = df['monto_contrato'].fillna('0.00').str.strip().str.extract(r'[-+]?\$?([\d.,]+)').replace({',': ''}, regex=True).fillna(0).astype(float)  # Extrae valores numéricos

    # Limpiar comuna
    df.loc[:, 'comuna'] = pd.to_numeric(df['comuna'], errors='coerce').fillna(0).astype(int)

    # Limpiar fecha_inicio y fecha_fin_inicial
    df.loc[:, 'fecha_inicio'] = df['fecha_inicio'].apply(lambda x: None if pd.isna(x) else x)
    df.loc[:, 'fecha_fin_inicial'] = df['fecha_fin_inicial'].apply(lambda x: None if pd.isna(x) else x)

    # Limpiar plazo_meses
    df.loc[:, 'plazo_meses'] = (
        df['plazo_meses'].astype(str)
        .str.replace(r'[^0-9,]', '', regex=True)
        .str.replace(',', '.')
        .replace('', 0)
        .fillna(0).astype(float)
    )

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

    df.loc[:, 'porcentaje_avance'] = df['porcentaje_avance'].apply(limpiar_porcentaje)
    df.loc[:, 'porcentaje_avance'] = df['porcentaje_avance'].clip(0, 100)

    # Limpiar licitacion_oferta_empresa
    df.loc[:, 'licitacion_oferta_empresa'] = df['licitacion_oferta_empresa'].str.strip()

    # Limpiar cuit_contratista
    df.loc[:, 'cuit_contratista'] = df['cuit_contratista'].astype(str)
    df.loc[:, 'cuit_contratista'] = df['cuit_contratista'].str.replace(r'[\n;]', ',', regex=True)
    df.loc[:, 'cuit_contratista'] = df['cuit_contratista'].str.replace(r'[^0-9,]', '', regex=True)

    # Limpiar contratacion_tipo
    df.loc[:, 'contratacion_tipo'] = df['contratacion_tipo'].astype(str)
    df.loc[:, 'contratacion_tipo'] = df['contratacion_tipo'].str.replace('-', '')  # Remover guiones

    return df

# Lista de columnas de interés
columnas_interes = [
    'tipo', 'nombre', 'etapa', 'area_responsable', 'descripcion', 
    'monto_contrato', 'barrio', 'comuna', 'fecha_inicio', 
    'fecha_fin_inicial', 'plazo_meses', 'porcentaje_avance', 
    'licitacion_oferta_empresa', 'cuit_contratista',
    'contratacion_tipo', 'nro_contratacion', 'mano_obra', 'expediente-numero', 
    'financiamiento'
]
