import pandas as pd
from recom_clips import *
import random
from classes import Visitant
from generacio.generacio_instancies import assign_salas, parse_cuadros

def simulate_responses():
    first_visit = random.choice([True, False])
    visitas = 0 if first_visit else random.randint(1, 10)

    # Restricción: Menores de 16 no pueden ir solos
    # edat sigue una distribución normal centrada en 30 años con desviación estándar de 15 años
    edat = int(round(random.gauss(30, 15)))

    if edat < 16:
        companyia = random.choice(["couple", "family", "group"])
    else:
        companyia = random.choice(["alone", "couple", "family", "group"])

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
    interessos_autor = random.sample(
        [
            "ignacio-pinazo-camarlench", "fillol-granell-antonio", "federico-de-madrazo",
            "diego-rodriguez-de-silva-y-velazquez", "tiziano-vecellio", "joaquin-sorolla",
            "fiodor-rokotov", "peter-paul-rubens", "rembrandt-van-rijn", "pieter-bruegel-el-vell",
            "j-m-w-turner", "leonardo-da-vinci", "rosa-bonheur", "winslow-homer",
            "edouard-vuillard", "charles-burchfield", "ben-shahn", "sandro-botticelli",
            "salvador-dali", "edvard-munch", "edouard-manet", "hieronymus-bosch",
            "johannes-vermeer", "eugene-delacroix", "not-sure"
        ],
        random.randint(1, 3)  # Máximo 3 intereses
    )
    interessos_estils = random.sample(
        ["modernisme", "romanticisme", "barroc", "renaixement", "impressionisme",
         "realisme", "contemporani", "surrealisme", "expressionisme", "not-sure"],
        random.randint(1, 3)  # Máximo 3 intereses
    )

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
        interessos_estils=interessos_estils
    )

file_path = "data/cuadros.txt"  # Cambia la ruta al archivo real
quadres, autores = parse_cuadros(file_path)
salas = assign_salas(quadres)

def simulate_multiple_visits(id, num_visits):
    """
    Función para simular múltiples visitas de un usuario, generando una ruta y puntuación para cada una.
    """
    visitante = simulate_responses()  # Generamos un visitante único
    visitas = []
    
    for num_visita in range(num_visits):  # Generamos varios registros de visitas para el mismo visitante
        visitante.dies = random.randint(1, 10)  # Cambiamos el número de días de visita
        visitante.hores = random.randint(1, 8)
        if visitante.edat < 16:
            visitante.companyia = random.choice(["couple", "family", "group"])
        else:
            visitante.companyia = random.choice(["alone", "couple", "family", "group"])

        show_visitor_classification(visitante)
        ruta = recommend_route(visitante, rutes)  # Asignamos una ruta
        refine_route(ruta, visitante, quadres)  # Refinamos la ruta basada en el visitante
        show_paintings_by_rooms(ruta, salas, quadres, visitante)  # Mostramos las pinturas por salas
        puntuacio_ruta = int(random.gauss(3, 1.5))  # Puntuación aleatoria de la ruta (distribución normal)
        
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
            'ruta': ruta,
            'puntuacio_ruta': puntuacio_ruta
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


df = pd.DataFrame(base_de_casos)

# Guardamos el DataFrame en un archivo CSV
df.to_csv('data/base_de_dades.csv', index=False)

print("Base de datos guardada en 'base_de_dades.csv'")

