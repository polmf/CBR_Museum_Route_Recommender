import pandas as pd
from recom_clips import *
import random
from classes import *
import json

# Cargar la base de datos
def load_database():
    df = pd.read_csv("artworks_data/artworks_final.csv")
    return df

# Función auxiliar para obtener valores únicos de una columna
def get_unique_options(df, column_name):
    return df[column_name].dropna().unique().tolist()

# Generar intereses aleatorios
def generate_random_interests(options, max_choices=3):
    return random.sample(options, random.randint(1, max_choices))


def simulate_responses(options_autor, options_estils, options_type):
    first_visit = random.choice([True, False])
    visitas = 0 if first_visit else random.randint(1, 10)

    edat = int(round(random.gauss(30, 15)))
    companyia = "group" if edat < 16 else random.choice(["alone", "group"])

    dies = random.randint(1, 10)
    hores = random.randint(1, 12)
    estudis = random.choice([True, False])
    coneixement = random.randint(1, 10)

    if estudis and coneixement > 7:
        quizz = min(6, max(0, random.gauss(5, 1)))
    else:
        quizz = random.randint(0, 6)

    quizz = int(round(quizz))
    
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
        interessos_type=interessos_type
    )


# Leer archivos JSON
with open('data/quadres.json', 'r', encoding='utf-8') as f_quadres:
    quadres_data = json.load(f_quadres)
    quadres = [Quadre.from_dict(data) for data in quadres_data]

with open('data/sales.json', 'r', encoding='utf-8') as f_sales:
    sales_data = json.load(f_sales)
    sales = {sala_id: Sala.from_dict(data) for sala_id, data in sales_data.items()}

with open('data/autors.json', 'r', encoding='utf-8') as f_autores:
    autores_data = json.load(f_autores)
    autors = {autor_nom: Autor.from_dict(data) for autor_nom, data in autores_data.items()}

df = load_database()

options_autor = get_unique_options(df, "Artist")
options_estils = get_unique_options(df, "Style")
options_type = get_unique_options(df, "Classification")


def simulate_multiple_visits(id, num_visits):
    visitante = simulate_responses(options_autor, options_estils, options_type)
    visitas = []
    
    for num_visita in range(num_visits):
        visitante.dies = random.randint(1, 10)
        visitante.hores = random.randint(1, 8)
        visitante.companyia = "group" if visitante.edat < 16 else random.choice(["alone", "group"])

        rutes = rutes_predeterminades(quadres)
        knowledge_factor = show_visitor_classification(visitante)
        ruta = recommend_route(visitante, rutes)
        refine_route(ruta, rutes, visitante, quadres, knowledge_factor)
        dies_ruta = show_paintings_by_rooms_sense_prints(ruta, visitante, knowledge_factor)
        puntuacio_ruta = int(random.gauss(3, 1.5))

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
            'visitant_interessos_tipus': visitante.interessos_type,
            'ruta': ruta.nom,
            'ruta_quadres': dies_ruta,
            'ruta_temps': round(ruta.temps),
            'puntuacio_ruta': puntuacio_ruta
        })
        
    return visitas


base_de_casos = []

# Simular visitantes
num_visitants = 500
for visitant_id, _ in enumerate(range(num_visitants)):
    visitas = simulate_multiple_visits(visitant_id, num_visits=int(max(1, (random.gauss(1, 3)))))
    print(f"Visitante {visitant_id} - {len(visitas)} visitas simuladas.")
    print("="*50)
    base_de_casos.extend(visitas)

# Guardar en JSON
output_path = 'data/base_de_dades_final.json'

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(base_de_casos, f, indent=4, ensure_ascii=False)

print(f"Base de datos guardada en '{output_path}'")
