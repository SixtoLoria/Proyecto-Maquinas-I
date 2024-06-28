import pandas as pd
import numpy as np

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
energia_mensual_kWh = (1/7) * (1/12000) * df['Potencia'].sum()      # muestras cada 5 min, convertido a kWh
potencia_mensual_kW = df['Potencia'].mean()   / 1000                # Promedio de potencia en Kwatts

print(f"Energía mensual en kWh: {energia_mensual_kWh:.2f}")
print(f"Potencia mensual en KW: {potencia_mensual_kW:.2f}")

Costo = 0

energia_anual_kWh = energia_mensual_kWh * 12
potencia_anual_kW = potencia_mensual_kW * 12

# ------------------- calculo del costo -----------------

if energia_mensual_kWh > 3000 and potencia_mensual_kW <= 8:
    Costo = energia_mensual_kWh * 46.03 + 59639.20
elif energia_mensual_kWh > 3000 and potencia_mensual_kW > 8:
    Costo = energia_mensual_kWh * 46.03 + (potencia_mensual_kW * 7454.90)
    
else:
    Costo = energia_mensual_kWh * 79.96
    
    
print(f"El costo es {Costo:.2f}")


# ------------------- calculo de perdidas -----------------
P_FE = 1650 
P_cu = 9500 
S_nom = 1000 * 10 ** 3 
fp = 0.9  # nominal

Perdidas = P_FE + P_cu * (df['Potencia'].mean()/S_nom * fp) ** 2  # en wats

Perdidas_kW = Perdidas / 1000


print(f"Las perdidas son en kW: {Perdidas_kW:.2f}")

# ------------------- calculo del costo con perdidas -----------------

if energia_mensual_kWh > 3000 and potencia_mensual_kW <= 8:
    
    Costo_P = (energia_mensual_kWh + Perdidas_kW) * 46.03 + 59639.20 * (1/7) * (1/12000)
    
elif energia_mensual_kWh > 3000 and (potencia_mensual_kW + Perdidas_kW) > 8:
    Costo_P = (energia_mensual_kWh + Perdidas_kW) * 46.03 + (potencia_mensual_kW * 7454.90) * (1/7) * (1/12000)
    
else:
    Costo_P = (energia_mensual_kWh + Perdidas_kW) * 79.96
    
print(f"El costo es considerando perdidas es: {Costo_P:.2f}")