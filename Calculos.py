""" 
Codigo para realizar a los consumos del exel


necesario instalar: pip install openpyxl
"""

import pandas as pd


# Convertir el archivo Excel a dataframe
df = pd.read_excel('Gráfico_consumo_edificio_EIE.xlsx')

# Mostrar las primeras filas del dataframe
# print(df.head())

# --------------- calculo de eficiencia ----------------------
# Constantes:
P_FE = 1650 
P_cu = 9500 
S_nom = 1000 * 10 **3 
fp = 0.9  # nominal

# Extraer los valores de potencia (wats) de las columnas específicas por índice
ciclo_regular = df.iloc[:, 7]  # Columna 8
ciclo_verano = df.iloc[:, 8]   # Columna 9
interciclo = df.iloc[:, 9]     # Columna 10
sab_dom_fer = df.iloc[:, 10]   # Columna 11
examenes = df.iloc[:, 11]      # Columna 12



# Calcular eficiencia
n = ciclo_regular / (ciclo_regular + P_FE + P_cu * (ciclo_regular/(S_nom * fp)))

