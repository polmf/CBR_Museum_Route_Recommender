from datetime import datetime, timedelta
import pandas as pd
from recom_clips import *
import random
from classes import Visitant, Quadre, Sala, Autor
import numpy as np
import json

# Cargar la base de datos
def load_database():
    df = pd.read_csv("artworks_data/artworks_final.csv")
    return df

# Función auxiliar para obtener valores únicos de una columna
def get_unique_options(df, column_name):
    unique_values = df[column_name].dropna().unique().tolist()
    if 'not-sure' not in unique_values:
        unique_values.append('not-sure')
    return unique_values

# Generar intereses aleatorios
def generate_random_interests(options, max_choices=3):
    return random.sample(options, random.randint(1, max_choices))


# Rangs d'edat i pesos de la distribució segons les dades
age_ranges = [(6, 17), (18, 24), (25, 34), (35, 44), (45, 54), (55, 64), (65, 99)]
data = [
    3.0,  # Menors (6-17 anys), ajustat per afegir-los al total
    8.317,  # 18-24
    41.148,  # 25-34
    29.914,  # 35-44
    17.254,  # 45-54
    14.571,  # 55-64
    10.301   # 65+
]

# Normalització dels pesos
weights_normalized = np.array(data) / np.sum(data)

# Funció per generar una edat aleatòria segons el rang seleccionat
def generate_age():
    selected_range = np.random.choice(len(age_ranges), p=weights_normalized)
    age = np.random.randint(age_ranges[selected_range][0], age_ranges[selected_range][1] + 1)
    return age

def simulate_responses(options_autor, options_estils, options_type):
    first_visit = random.choice([True, False])
    visitas = 0 if first_visit else random.randint(1, 10)

    # Restricción: Menores de 16 no pueden ir solos
    edat = generate_age()

    if edat < 16:
        companyia = "group"
    else:
        companyia = random.choice(["alone", "group"])

    dies = random.randint(1, 10)
    hores = random.randint(1, 12)
    estudis = random.choice([True, False])
    coneixement = random.randint(1, 10)

    # Restricción: Si el usuario tiene estudios y alto conocimiento, puntaje del quizz más alto
    if estudis and coneixement > 7:
        quizz = min(6, max(0, random.gauss(5, 1)))  # Centrado en 5 con algo de variabilidad
    else:
        quizz = random.randint(0, 6)  # Rango completo si no cumple los criterios

    quizz = int(round(quizz))  # Aseguramos que sea un entero
    
    # Generar intereses aleatorios
    interessos_autor = generate_random_interests(options_autor, 3)
    interessos_estils = generate_random_interests(options_estils, 3)
    interessos_type = generate_random_interests(options_type, 3)

    return Visitant(
        visites=visitas,
        companyia=companyia,
        dies=dies,
        hores=hores,
        edat=edat,
        estudis=estudis,
        coneixement=coneixement,
        quizz=quizz,
        interessos_autor=interessos_autor,
        interessos_estils=interessos_estils,
        interessos_tipus=interessos_type
    )

with open('data/quadres.json', 'r', encoding='utf-8') as f_quadres:
        quadres_data = json.load(f_quadres)
        quadres = [Quadre.from_dict(data) for data in quadres_data]

    # Leer y convertir el archivo de las sales
with open('data/sales.json', 'r', encoding='utf-8') as f_sales:
    sales_data = json.load(f_sales)
    sales = {sala_id: Sala.from_dict(data) for sala_id, data in sales_data.items()}

    # Leer y convertir el archivo de los autores
with open('data/autors.json', 'r', encoding='utf-8') as f_autores:
    autores_data = json.load(f_autores)
    autors = {autor_nom: Autor.from_dict(data) for autor_nom, data in autores_data.items()}
    
df = load_database()
    
# Obtener opciones dinámicamente
options_autor = get_unique_options(df, "Artist")
options_estils = get_unique_options(df, "Style")
options_type = get_unique_options(df, "Classification")

def simulate_multiple_visits(id, num_visits):
    """
    Función para simular múltiples visitas de un usuario, generando una ruta y puntuación para cada una.
    """
    visitante = simulate_responses(options_autor, options_estils, options_type)  # Generamos un visitante único
    visitas = []
    
    for num_visita in range(num_visits):  # Generamos varios registros de visitas para el mismo visitante
        visitante.dies = random.randint(1, 6)  # Cambiamos el número de días de visita
        visitante.hores = random.randint(1, 6)
        if visitante.edat < 16:
            visitante.companyia = "group"
        else:
            visitante.companyia = random.choice(["alone", "group"])

        rutes = rutes_predeterminades(quadres)
        knowledge_factor = show_visitor_classification(visitante)
        ruta = recommend_route(visitante, rutes)  # Asignamos una ruta
        refine_route(ruta, rutes, visitante, quadres, knowledge_factor)  # Refinamos la ruta basada en el visitante
        dies_ruta = show_paintings_by_rooms_sense_prints(ruta, visitante, knowledge_factor)  # Mostramos las pinturas por salas
        puntuacio_ruta = int(random.gauss(3, 1.5))  # Puntuación aleatoria de la ruta (distribución normal)
        
        # clip para asegurar que la puntuación esté en el rango [0, 5]
        puntuacio_ruta = min(5, max(0, puntuacio_ruta))

        data_ultim_us = (datetime.now() - timedelta(days=random.randint(0, 730))).strftime("%Y-%m-%d")

        recompte_utilitzat = max(1, int(random.gammavariate(2, 2)))  # Al menos 1
        
        # Almacenamos la visita con la ruta y su puntuación
        visitas.append({
            'visitante_id': id,
            'visitant_edat': visitante.edat,
            'visitant_visites': num_visita,
            'visitant_dies': visitante.dies,
            'visitant_hores': visitante.hores,
            'visitant_companyia': visitante.companyia,
            'visitant_estudis': visitante.estudis,
            'visitant_coneixement': visitante.coneixements,
            'visitant_quizz': visitante.quizz,
            'visitant_interessos_autor': visitante.interessos_autor,
            'visitant_interessos_estils': visitante.interessos_estils,
            'visitant_interessos_tipus': visitante.interessos_tipus,
            'ruta': ruta.nom,
            'ruta_quadres': dies_ruta,
            'ruta_quadres_list': ruta.quadres,
            'ruta_temps': round(ruta.temps),
            'puntuacio_ruta': puntuacio_ruta,
            'data_ultim_us': data_ultim_us,
            'recompte_utilitzat': recompte_utilitzat
        })
        
    return visitas

base_de_casos = []

# Simulamos múltiples visitas por usuario
num_visitants = 500  # Número de visitantes a simular
for visitant_id, _ in enumerate(range(num_visitants)):
    visitas = simulate_multiple_visits(visitant_id, num_visits=int(max(1, (random.gauss(1, 3)))))  # Simulamos múltiples visitas
    print(f"Visitante {visitant_id} - {len(visitas)} visitas simuladas.")
    print("="*50)
    base_de_casos.extend(visitas)


# Guardar en JSON
output_path = 'data/base_de_dades_final.json'

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(base_de_casos, f, indent=4, ensure_ascii=False)

print(f"Base de datos guardada en '{output_path}'")
