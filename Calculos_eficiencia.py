import pandas as pd
import matplotlib.pyplot as plt

# Convertir el archivo Excel a dataframe
df = pd.read_excel('Gráfico_consumo_edificio_EIE.xlsx')

# Mostrar las primeras filas del dataframe
# print(df.head())

# --------------- cálculo de eficiencia ----------------------
# Constantes:
P_FE = 1650 
P_cu = 9500 
S_nom = 1000 * 10 ** 3 
fp = 0.9  # nominal

# Lista de índices de las columnas de datos de consumo de potencia
column_indices = [7, 8, 9, 10, 11]  # Columnas 8 a 12

# Diccionario para almacenar los resultados de eficiencia
eficiencia = {}
column_labels = {
    7: 'Ciclo regular',
    8: 'Ciclo verano',
    9: 'Interciclo',
    10: 'Feriados y fines de semana',
    11: 'Exámenes'
}

# Calcular eficiencia para cada columna
for idx in column_indices:
    # Extraer los valores de potencia (watts) de la columna específica y convertirlos a numéricos
    potencia = pd.to_numeric(df.iloc[:, idx], errors='coerce')
    
    # Calcular la eficiencia
    n = potencia / (potencia + P_FE + P_cu * (potencia / (S_nom * fp)))
    
    # Almacenar el resultado en el diccionario
    eficiencia[column_labels[idx]] = n

# Extraer las horas de la columna 7 y convertirlas a cadenas de texto
horas = df.iloc[:, 6].astype(str)

# Graficar las eficiencias
plt.figure(figsize=(14, 8))

for key, value in eficiencia.items():
    plt.plot(horas, value, label=key)

plt.xlabel('Horas')
plt.ylabel('Eficiencia')
plt.title('Eficiencia alrededor del dia')
plt.legend()
plt.grid(True)

# Configurar las etiquetas del eje x para mostrar solo algunas
step = len(horas) // 12  # Mostrar aproximadamente 12 etiquetas
plt.xticks(horas[::step], rotation=45)  # Rotar las etiquetas del eje x para mejor legibilidad

plt.tight_layout()  # Ajustar el diseño para que todo se vea correctamente
plt.show()
