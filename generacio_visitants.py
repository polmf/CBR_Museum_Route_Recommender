from recom_clips import *
import random

def simulate_responses():
    first_visit = random.choice([True, False])
    visitas = 0 if first_visit else random.randint(1, 10)
    companyia = random.choice(["alone", "couple", "family", "group"])
    dies = random.randint(1, 10)
    hores = random.randint(1, 12)
    edat = random.randint(0, 110)
    estudis = random.choice([True, False])
    coneixement = random.randint(1, 10)
    quizz = random.randint(0, 6)  # Simula un puntaje del quiz entre 0 y 6
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




visitantes = [simulate_responses() for _ in range(10)]
file_path = "cuadros.txt"  # Cambia la ruta al archivo real
quadres, autores = parse_cuadros(file_path)
salas = assign_salas(quadres)

samples = []
for visitante in visitantes:

    show_visitor_classification(visitante)
    ruta = recommend_route(visitante, rutes)
    refine_route(ruta, visitante, quadres)
    show_paintings_by_rooms(ruta, salas, quadres, visitante)
    puntuacio_ruta = random.randint(1,5)
    samples.append([visitante, ruta, puntuacio_ruta])

