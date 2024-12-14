import json
import matplotlib.pyplot as plt
import seaborn as sns
from classes import Quadre
import numpy as np

# Cargar los datos desde el archivo JSON
with open('data/quadres.json', 'r', encoding='utf-8') as f_quadres:
    quadres_data = json.load(f_quadres)
    data = [Quadre.from_dict(data) for data in quadres_data]

# Inicializamos las variables para los valores más altos
max_relevancia = -float('inf')
max_complexitat = -float('inf')
cuadro_max_relevancia = ""
cuadro_max_complexitat = ""

# Creamos listas para graficar
nombres = []
relevancias = []
complexitats = []
dim_cm2s = []

# Recorremos todos los cuadros y recopilamos datos
for cuadro in data:
    nombres.append(cuadro.nom)
    relevancias.append(cuadro.rellevancia)
    complexitats.append(cuadro.complexitat)
    dim_cm2s.append(cuadro.dim_cm2)

    # Encontramos valores máximos
    if cuadro.rellevancia > max_relevancia:
        max_relevancia = cuadro.rellevancia
        cuadro_max_relevancia = cuadro.nom
    
    if cuadro.complexitat > max_complexitat:
        max_complexitat = cuadro.complexitat
        cuadro_max_complexitat = cuadro.nom

# Mostramos los resultados de los máximos
print(f"El cuadro con mayor relevancia es: {cuadro_max_relevancia} con relevancia de {max_relevancia}")
print(f"El cuadro con mayor complejidad es: {cuadro_max_complexitat} con complejidad de {max_complexitat}")
print(f"Media de dim_cm2 {np.mean(dim_cm2s)}")
# Configuramos Seaborn para los gráficos
sns.set(style="whitegrid")

# Gráfico de distribución de Relevancia
plt.figure(figsize=(12, 6))
sns.histplot(relevancias, kde=True, bins=15, color="skyblue")
plt.title("Distribución de Relevancia")
plt.xlabel("Relevancia")
plt.ylabel("Frecuencia")
plt.show()

# Gráfico de distribución de Complejidad
plt.figure(figsize=(12, 6))
sns.histplot(complexitats, kde=True, bins=15, color="lightcoral")
plt.title("Distribución de Complejidad")
plt.xlabel("Complejidad")
plt.ylabel("Frecuencia")
plt.show()

# 1. Histograma de la distribución de dim_cm2
plt.figure(figsize=(12, 6))
sns.histplot(dim_cm2s, kde=True, bins=15, color="lightblue")
plt.title("Distribución de Tamaño (dim_cm2)")
plt.xlabel("Tamaño en cm² (dim_cm2)")
plt.ylabel("Frecuencia")
plt.show()

