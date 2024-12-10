import json
from classes import Quadre

with open('data/quadres.json', 'r', encoding='utf-8') as f_quadres:
        quadres_data = json.load(f_quadres)
        data = [Quadre.from_dict(data) for data in quadres_data]

# Inicializamos las variables para los valores más altos
max_relevancia = -float('inf')  # Para asegurarnos de que cualquier valor encontrado será mayor
max_complexitat = -float('inf')
cuadro_max_relevancia = ""
cuadro_max_complexitat = ""

# Recorremos todos los cuadros
for cuadro in data:
    if cuadro.rellevancia > max_relevancia:
        max_relevancia = cuadro.rellevancia
        cuadro_max_relevancia = cuadro.nom
    
    if cuadro.complexitat >= max_complexitat:
        max_complexitat = cuadro.complexitat
        cuadro_max_complexitat = cuadro.nom

# Mostramos los resultados
print(f"El cuadro con mayor relevancia es: {cuadro_max_relevancia} con relevancia de {max_relevancia}")
print(f"El cuadro con mayor complejidad es: {cuadro_max_complexitat} con complejidad de {max_complexitat}")
