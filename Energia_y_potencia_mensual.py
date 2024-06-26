import pandas as pd

# Leer el archivo Excel con los datos
df = pd.read_excel('Gráfico_consumo_edificio_EIE.xlsx', header=None, names=['Fecha', 'Hora', 'tipo de dia', 'Potencia'])

# Eliminar filas con NaN en 'Fecha' o 'Hora'
df = df.dropna(subset=['Fecha', 'Hora'])

# Asegurarse de que 'Fecha' y 'Hora' sean cadenas
df['Fecha'] = df['Fecha'].astype(str)
df['Hora'] = df['Hora'].astype(str)

# Filtrar valores no numéricos en 'Potencia' y convertir a números si es posible
df['Potencia'] = pd.to_numeric(df['Potencia'], errors='coerce')

# Eliminar filas con NaN en 'Potencia' si es necesario
df = df.dropna(subset=['Potencia'])

# Calcular energía mensual y potencia mensual en watts
energia_mensual_kWh = df['Potencia'].sum() * 720 / 1000 / 1000  # 720 horas por mes, convertido a kWh
potencia_mensual_W = df['Potencia'].mean()                      # Promedio de potencia en watts

print(f"Energía mensual en kWh: {energia_mensual_kWh}")
print(f"Potencia mensual en W: {potencia_mensual_W}")
