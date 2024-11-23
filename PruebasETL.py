import pandas as pd

# Supongamos que tienes un DataFrame llamado df
df = pd.DataFrame({
    'columna1': ['valor1', 'valor2', 'valor3'],
    'columna2': ['valor4', 'valor5', 'valor6']
})

# Reemplazar 'valor1' por 'nuevo_valor1' en todo el DataFrame
df = df.replace('valor1', 'nuevo_valor1')

# Reemplazar múltiples valores en una columna específica
df['columna1'] = df['columna1'].replace({'valor2': 'nuevo_valor2', 'valor3': 'nuevo_valor3'})

print(df)