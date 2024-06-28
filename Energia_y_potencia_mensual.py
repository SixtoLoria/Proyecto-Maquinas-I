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

print(f"La energia anual son en kW:  {energia_anual_kWh:.2f}")
print(f"La potencia anual son en kW: {potencia_anual_kW:.2f}")

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

Perdidas_mensuales_kWh = (1/7) * (1/12000) * ( P_FE + P_cu * (df['Potencia'].mean()/S_nom * fp) ** 2 ) # en wats

Perdidas_mensuales_kW = ( P_FE + P_cu * (df['Potencia'].mean()/S_nom * fp) ** 2 ) / 1000


print(f"Las perdidas mensuales son en kW:  {Perdidas_mensuales_kW:.2f}")
print(f"Las perdidas mensuales son en kWh: {Perdidas_mensuales_kW:.2f}")


# ------------------- calculo del costo con perdidas -----------------

kWh_totales = energia_mensual_kWh + Perdidas_mensuales_kWh
kW_totales = potencia_mensual_kW + Perdidas_mensuales_kW

if kWh_totales > 3000 and kW_totales <= 8:
    
    Costo_P = (kWh_totales) * 46.03 + 59639.20
    
elif (kWh_totales) > 3000 and (kW_totales) > 8:
    Costo_P = (kWh_totales) * 46.03 + ((kW_totales) * 7454.90)
else:
    Costo_P = (kWh_totales) * 79.96
    
print(f"El costo es considerando perdidas es: {Costo_P:.2f}")
