import pandas as pd
import numpy as np

# Limpieza de datos del grupo 3
df = pd.read_csv('https://cdn.buenosaires.gob.ar/datosabiertos/datasets/secretaria-general-y-relaciones-internacionales/ba-obras/observatorio-de-obras-urbanas.csv', sep=";", index_col=0, encoding='latin-1')

columnas_grupo3 = ['fecha_inicio', 'fecha_fin_inicial', 'plazo_meses', 'porcentaje_avance']

def limpiar_datos(df):
    # Convierto columnas de [´fecha_inicio', 'fecha_fin_inicial'] a formato datetime
    df['fecha_inicio'] = pd.to_datetime(df['fecha_inicio'], errors='coerce')
    df['fecha_fin_inicial'] = pd.to_datetime(df['fecha_fin_inicial'], errors='coerce')

    # Convierto columnas ['plazo_meses'] a int y antes reemplazo los valores nulos con 0
    df['plazo_meses'] = pd.to_numeric(df['plazo_meses'], errors='coerce')
    df['plazo_meses'] = df['plazo_meses'].fillna(0).astype(int)

    # Reemplazo los valores nulos en la columna ['plazo_meses'] con la mediana 
    df['plazo_meses'] = df['plazo_meses'].fillna(df['plazo_meses'].median())

    def limpiar_porcentaje(valor):
        # Si el valor es nulo (NaN), la función lo retorna tal cual
        if pd.isna(valor):
            return np.nan
        if isinstance(valor, (int, float)):
            # Si el valor es un float, lo multiplico por 100 
            return valor * 100 if valor <= 1 else valor
        if isinstance(valor, str):
            # Si el valor es un string, elimina el '%' y elimina espacios en blanco
            valor = valor.replace('%', '').strip()
            try:
                # Conversión a float
                return float(valor)
            except ValueError:
                # Si la conversión falla, devuelve NaN
                return np.nan
        return np.nan

    df['porcentaje_avance'] = df['porcentaje_avance'].apply(limpiar_porcentaje)
    
    # Utilizo clip para asegurar que los porcentajes estén entre 0 y 100
    df['porcentaje_avance'] = df['porcentaje_avance'].clip(0, 100)

    # Elimino cualquier fila restante que contenga valores nulos
    df = df.dropna(subset=['fecha_inicio', 'fecha_fin_inicial', 'plazo_meses', 'porcentaje_avance'])

    return df
# ---------------------------------------------------------------------------------------------------
df_limpio = limpiar_datos(df)

df_final = df_limpio[columnas_grupo3]

# Mostrar las primeras filas de las columnas
print("\nPrimeras filas de las columnas del grupo 3:")
print(df_final.head())

