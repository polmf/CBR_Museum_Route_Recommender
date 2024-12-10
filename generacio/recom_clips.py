from classes import *
import random
import json
class Ruta:
    def __init__(self, nom, instancies, quadres = [], temps=0.0):
        self.nom = nom
        self.instancies = instancies
        self.quadres = quadres
        self.temps = temps

    def get_nom(self):
        return self.nom
    
    def get_quadres(self):
        return self.quadres
    
    def get_temps(self):
        return self.temps

def calculate_observation_time_pred(painting):
    complexity = painting.complexitat
    dim_cm2 = painting.dim_cm2
    relevance = painting.rellevancia
    
    
    base_time = 1.0 if dim_cm2 < 5007 else 2.0

    complexity_factor = (
        1.1 if complexity <= 1 else
        1.2 if complexity <= 2 else
        1.3 if complexity <= 3 else
        1.4 if complexity <= 4 else
        1.5
    )

    relevance_factor = (
        1.1 if relevance <= 1 else
        1.2 if relevance <= 2 else
        1.3 if relevance <= 3 else
        1.4 if relevance <= 4 else
        1.5
    )

    total_time = (base_time * complexity_factor * relevance_factor)
    return total_time

import random

def rutes_predeterminades(quadres):
    rutes = []
    quadres_rellevants = [quadre for quadre in quadres if quadre.rellevancia >= 8]
    quadres_poc_rellevants = [quadre for quadre in quadres if quadre.rellevancia <= 3]
    quadres_poc_mig_rellevants = [quadre for quadre in quadres if quadre.rellevancia < 3 and quadre.rellevancia <= 5.5]
    quadres_mig_rellevants = [quadre for quadre in quadres if quadre.rellevancia < 5.5 and quadre.rellevancia <= 7.9]
    quadres_complexitat = [quadre for quadre in quadres if quadre.complexitat >= 8]
    quadres_poc_complexitat = [quadre for quadre in quadres if quadre.complexitat <= 3]
    quadres_poc_mig_complexitat = [quadre for quadre in quadres if quadre.complexitat < 3 and quadre.complexitat <= 5.5]
    quadres_mig_complexitat = [quadre for quadre in quadres if quadre.complexitat < 5.5 and quadre.complexitat <= 7.9]
    
    # Función para seleccionar cuadros sin repetir dentro de la misma ruta
    def seleccionar_quadres(quadres_list, num_quadres, cuadros_seleccionados_ruta):
        disponibles = [quadre for quadre in quadres_list if quadre.nom not in cuadros_seleccionados_ruta]
        seleccionados = random.sample(disponibles, min(num_quadres, len(disponibles)))
        cuadros_seleccionados_ruta.update(quadre.nom for quadre in seleccionados)
        return seleccionados
    
    # Ruta 1
    cuadros_seleccionados_ruta1 = set()  # Conjunto para la ruta 1
    ruta1 = Ruta(
        nom="ruta1",
        instancies=seleccionar_quadres(quadres_rellevants, 15, cuadros_seleccionados_ruta1) + seleccionar_quadres(quadres_poc_complexitat, 10, cuadros_seleccionados_ruta1),
    )
    ruta1.quadres = [quadre.nom for quadre in ruta1.instancies]
    ruta1.temps = sum(calculate_observation_time_pred(quadre) for quadre in ruta1.instancies)
    rutes.append(ruta1)

    # Ruta 2
    cuadros_seleccionados_ruta2 = set()  # Conjunto para la ruta 2
    ruta2 = Ruta(
        nom="ruta2",
        instancies=seleccionar_quadres(quadres_rellevants, 15, cuadros_seleccionados_ruta2) + seleccionar_quadres(quadres_poc_mig_complexitat, 10, cuadros_seleccionados_ruta2),
    )
    ruta2.quadres = [quadre.nom for quadre in ruta2.instancies]
    ruta2.temps = sum(calculate_observation_time_pred(quadre) for quadre in ruta2.instancies)
    rutes.append(ruta2)

    # Ruta 3
    cuadros_seleccionados_ruta3 = set()  # Conjunto para la ruta 3
    ruta3 = Ruta(
        nom="ruta3",
        instancies=seleccionar_quadres(quadres_rellevants, 10, cuadros_seleccionados_ruta3) + seleccionar_quadres(quadres_mig_rellevants, 5, cuadros_seleccionados_ruta3) + seleccionar_quadres(quadres_poc_mig_complexitat, 10, cuadros_seleccionados_ruta3),
    )
    ruta3.quadres = [quadre.nom for quadre in ruta3.instancies]
    ruta3.temps = sum(calculate_observation_time_pred(quadre) for quadre in ruta3.instancies)
    rutes.append(ruta3)

    # Ruta 4
    cuadros_seleccionados_ruta4 = set()  # Conjunto para la ruta 4
    ruta4 = Ruta(
        nom="ruta4",
        instancies=seleccionar_quadres(quadres_rellevants, 5, cuadros_seleccionados_ruta4) + seleccionar_quadres(quadres_mig_rellevants, 5, cuadros_seleccionados_ruta4) + seleccionar_quadres(quadres_poc_mig_rellevants, 5, cuadros_seleccionados_ruta4) + seleccionar_quadres(quadres_mig_complexitat, 5, cuadros_seleccionados_ruta4) + seleccionar_quadres(quadres_complexitat, 5, cuadros_seleccionados_ruta4),
    )
    ruta4.quadres = [quadre.nom for quadre in ruta4.instancies]
    ruta4.temps = sum(calculate_observation_time_pred(quadre) for quadre in ruta4.instancies)
    rutes.append(ruta4)

    # Ruta 5
    cuadros_seleccionados_ruta5 = set()  # Conjunto para la ruta 5
    ruta5 = Ruta(
        nom="ruta5",
        instancies=seleccionar_quadres(quadres_rellevants, 25, cuadros_seleccionados_ruta5) + seleccionar_quadres(quadres_poc_complexitat, 10, cuadros_seleccionados_ruta5) + seleccionar_quadres(quadres_poc_mig_complexitat, 10, cuadros_seleccionados_ruta5),
    )
    ruta5.quadres = [quadre.nom for quadre in ruta5.instancies]
    ruta5.temps = sum(calculate_observation_time_pred(quadre) for quadre in ruta5.instancies)
    rutes.append(ruta5)

    # Ruta 6
    cuadros_seleccionados_ruta6 = set()  # Conjunto para la ruta 6
    ruta6 = Ruta(
        nom="ruta6",
        instancies=seleccionar_quadres(quadres_rellevants, 20, cuadros_seleccionados_ruta6) + seleccionar_quadres(quadres_mig_rellevants, 5, cuadros_seleccionados_ruta6) + seleccionar_quadres(quadres_poc_complexitat, 10, cuadros_seleccionados_ruta6) + seleccionar_quadres(quadres_poc_mig_complexitat, 10, cuadros_seleccionados_ruta6),
    )
    ruta6.quadres = [quadre.nom for quadre in ruta6.instancies]
    ruta6.temps = sum(calculate_observation_time_pred(quadre) for quadre in ruta6.instancies)
    rutes.append(ruta6)

    # Ruta 7
    cuadros_seleccionados_ruta7 = set()  # Conjunto para la ruta 7
    ruta7 = Ruta(
        nom="ruta7",
        instancies=seleccionar_quadres(quadres_rellevants, 10, cuadros_seleccionados_ruta7) + seleccionar_quadres(quadres_mig_rellevants, 10, cuadros_seleccionados_ruta7) + seleccionar_quadres(quadres_poc_mig_rellevants, 5, cuadros_seleccionados_ruta7) + seleccionar_quadres(quadres_poc_mig_complexitat, 15, cuadros_seleccionados_ruta7) + seleccionar_quadres(quadres_mig_complexitat, 5, cuadros_seleccionados_ruta7),
    )
    ruta7.quadres = [quadre.nom for quadre in ruta7.instancies]
    ruta7.temps = sum(calculate_observation_time_pred(quadre) for quadre in ruta7.instancies)
    rutes.append(ruta7)

    # Ruta 8
    cuadros_seleccionados_ruta8 = set()  # Conjunto para la ruta 8
    ruta8 = Ruta(
        nom="ruta8",
        instancies=seleccionar_quadres(quadres_rellevants, 10, cuadros_seleccionados_ruta8) + seleccionar_quadres(quadres_mig_rellevants, 10, cuadros_seleccionados_ruta8) + seleccionar_quadres(quadres_poc_mig_rellevants, 10, cuadros_seleccionados_ruta8) + seleccionar_quadres(quadres_poc_mig_complexitat, 10, cuadros_seleccionados_ruta8) + seleccionar_quadres(quadres_mig_complexitat, 10, cuadros_seleccionados_ruta8) + seleccionar_quadres(quadres_complexitat, 5, cuadros_seleccionados_ruta8),
    )
    ruta8.quadres = [quadre.nom for quadre in ruta8.instancies]
    ruta8.temps = sum(calculate_observation_time_pred(quadre) for quadre in ruta8.instancies)
    rutes.append(ruta8)

    # Ruta 9
    cuadros_seleccionados_ruta9 = set()  # Conjunto para la ruta 9
    ruta9 = Ruta(
        nom="ruta9",
        instancies=seleccionar_quadres(quadres_rellevants, 10, cuadros_seleccionados_ruta9) + seleccionar_quadres(quadres_mig_rellevants, 10, cuadros_seleccionados_ruta9) + seleccionar_quadres(quadres_poc_mig_rellevants, 10, cuadros_seleccionados_ruta9) + seleccionar_quadres(quadres_mig_complexitat, 5, cuadros_seleccionados_ruta9) + seleccionar_quadres(quadres_mig_complexitat, 10, cuadros_seleccionados_ruta9) + seleccionar_quadres(quadres_complexitat, 15, cuadros_seleccionados_ruta9),
    )
    ruta9.quadres = [quadre.nom for quadre in ruta9.instancies]
    ruta9.temps = sum(calculate_observation_time_pred(quadre) for quadre in ruta9.instancies)
    rutes.append(ruta9)

    # Ruta 10
    cuadros_seleccionados_ruta10 = set()  # Conjunto para la ruta 10
    ruta10 = Ruta(
        nom="ruta10",
        instancies=seleccionar_quadres(quadres_rellevants, 30, cuadros_seleccionados_ruta10) + seleccionar_quadres(quadres_mig_rellevants, 10, cuadros_seleccionados_ruta10) + seleccionar_quadres(quadres_poc_mig_complexitat, 10, cuadros_seleccionados_ruta10) + seleccionar_quadres(quadres_poc_complexitat, 15, cuadros_seleccionados_ruta10),
    )
    ruta10.quadres = [quadre.nom for quadre in ruta10.instancies]
    ruta10.temps = sum(calculate_observation_time_pred(quadre) for quadre in ruta10.instancies)
    rutes.append(ruta10)

    # Ruta 11
    cuadros_seleccionados_ruta11 = set()  # Conjunto para la ruta 11
    ruta11 = Ruta(
        nom="ruta11",
        instancies=seleccionar_quadres(quadres_rellevants, 25, cuadros_seleccionados_ruta11) + seleccionar_quadres(quadres_mig_rellevants, 10, cuadros_seleccionados_ruta11) + seleccionar_quadres(quadres_poc_mig_rellevants, 5, cuadros_seleccionados_ruta11) + seleccionar_quadres(quadres_poc_complexitat, 15, cuadros_seleccionados_ruta11)  + seleccionar_quadres(quadres_poc_mig_complexitat, 15, cuadros_seleccionados_ruta11) + seleccionar_quadres(quadres_mig_complexitat, 5, cuadros_seleccionados_ruta11),
    )
    ruta11.quadres = [quadre.nom for quadre in ruta11.instancies]
    ruta11.temps = sum(calculate_observation_time_pred(quadre) for quadre in ruta11.instancies)
    rutes.append(ruta11)

    # Ruta 12
    cuadros_seleccionados_ruta12 = set()  # Conjunto para la ruta 12
    ruta12 = Ruta(
        nom="ruta12",
        instancies=seleccionar_quadres(quadres_rellevants, 20, cuadros_seleccionados_ruta12) + seleccionar_quadres(quadres_mig_rellevants, 15, cuadros_seleccionados_ruta12) + seleccionar_quadres(quadres_poc_mig_rellevants, 10, cuadros_seleccionados_ruta12) + seleccionar_quadres(quadres_poc_mig_complexitat, 20, cuadros_seleccionados_ruta12) + seleccionar_quadres(quadres_mig_complexitat, 15, cuadros_seleccionados_ruta12),
    )
    ruta12.quadres = [quadre.nom for quadre in ruta12.instancies]
    ruta12.temps = sum(calculate_observation_time_pred(quadre) for quadre in ruta12.instancies)
    rutes.append(ruta12)

    # Ruta 13
    cuadros_seleccionados_ruta13 = set()  # Conjunto para la ruta 13
    ruta13 = Ruta(
        nom="ruta13",
        instancies=seleccionar_quadres(quadres_rellevants, 10, cuadros_seleccionados_ruta13) + seleccionar_quadres(quadres_mig_rellevants, 15, cuadros_seleccionados_ruta13) + seleccionar_quadres(quadres_poc_mig_rellevants, 15, cuadros_seleccionados_ruta13) + seleccionar_quadres(quadres_poc_rellevants, 5, cuadros_seleccionados_ruta13) + seleccionar_quadres(quadres_poc_mig_complexitat, 15, cuadros_seleccionados_ruta13) + seleccionar_quadres(quadres_mig_complexitat, 15, cuadros_seleccionados_ruta13) + seleccionar_quadres(quadres_complexitat, 10, cuadros_seleccionados_ruta13),
    )
    ruta13.quadres = [quadre.nom for quadre in ruta13.instancies]
    ruta13.temps = sum(calculate_observation_time_pred(quadre) for quadre in ruta13.instancies)
    rutes.append(ruta13)

    # Ruta 14
    cuadros_seleccionados_ruta14 = set()  # Conjunto para la ruta 14
    ruta14 = Ruta(
        nom="ruta14",
        instancies=seleccionar_quadres(quadres_rellevants, 10, cuadros_seleccionados_ruta14) + seleccionar_quadres(quadres_mig_rellevants, 15, cuadros_seleccionados_ruta14)  + seleccionar_quadres(quadres_poc_mig_rellevants, 15, cuadros_seleccionados_ruta14) + seleccionar_quadres(quadres_poc_rellevants, 5, cuadros_seleccionados_ruta14) + seleccionar_quadres(quadres_mig_complexitat, 10, cuadros_seleccionados_ruta14) + seleccionar_quadres(quadres_mig_complexitat, 15, cuadros_seleccionados_ruta14) + seleccionar_quadres(quadres_complexitat, 20, cuadros_seleccionados_ruta14),
    )
    ruta14.quadres = [quadre.nom for quadre in ruta14.instancies]
    ruta14.temps = sum(calculate_observation_time_pred(quadre) for quadre in ruta14.instancies)
    rutes.append(ruta14)

    return rutes



def yes_or_no(question):
    answer = input(question).strip().lower()
    while answer not in ["yes", "no"]:
        print("Please answer with 'yes' or 'no'.")
        answer = input(question).strip().lower()
    return answer == "yes"

def ask_question_numerical(question, min_value, max_value):
    while True:
        try:
            response = int(input(question))
            if min_value <= response <= max_value:
                return response
            else:
                print(f"Please enter a number between {min_value} and {max_value}.")
        except ValueError:
            print("Please enter a valid number.")

def ask_question(question, options):
    answer = input(f"{question} ({', '.join(options)}) ").strip().lower()
    while answer not in options:
        print(f"Invalid answer. Please choose one of {', '.join(options)}.")
        answer = input(f"{question} ({', '.join(options)}) ").strip().lower()
    return answer

def ask_multiple_choice(question, correct_answer, options):
    print(question)
    response = input(f"Your answer ({', '.join(options)}): ").strip().lower()
    while response not in options:
        print(f"Invalid answer. Choose one of {', '.join(options)}.")
        response = input(f"Your answer ({', '.join(options)}): ").strip().lower()
    return response

def ask_multiple_options(question, options, limit):
    print(f"{question} ({', '.join(options)})")
    selected = input(f"Please select up to {limit} options: ").strip().lower().split(',')
    selected = [opt.strip() for opt in selected if opt.strip() in options]
    while len(selected) > limit:
        print(f"You can select at most {limit} options.")
        selected = input(f"Please select up to {limit} options: ").strip().lower().split(',')
        selected = [opt.strip() for opt in selected if opt.strip() in options]
    return selected

# Funciones para las preguntas del visitante

def numero_dies_visites():
    print("Hello! My name is Muse, and I'm here to make your experience in the museum better.")
    print("In order to personalize your experience, I need you to answer a few questions.")
    print("It will only take a couple of minutes. Ready? Let's go!")
    first_visit = yes_or_no("Is this your first time visiting the museum (yes/no)? ")
    return first_visit

def primera_visita(first_visit):
    if first_visit:
        return 0
    return ask_question_numerical("How many times have you been here before? (1-10) ", 1, 10)

def amb_qui_vens():
    return ask_question("Who are you visiting the museum with? (alone/group) ", ["alone", "group"])

def dies_visita():
    return ask_question_numerical("How many days are you planning on coming to the museum (1-10)? ", 1, 10)

def hores_visita_per_dia():
    return ask_question_numerical("How many hours do you want to spend in the museum each day? (1-12) ", 1, 12)

def age_question(company):
    question = "How old are you? (0-110) " if company == "alone" else "How old is the youngest person in the group? (0-110) "
    return ask_question_numerical(question, 0, 110)

def studies():
    return yes_or_no("Have you studied any art-related subjects, such as fine arts, art history, or others? (yes/no) ")

def art_knowledge():
    return ask_question_numerical("On a scale from 1 to 10, how would you rate your art knowledge? (1-10) ", 1, 10)

# Quiz logic
def start_quiz():
    print("Next, let's get ready for a fun little quiz to see how much you know about art!")
    print("No pressure—this is all about learning and having a good time.")
    score = 0
    questions = [
        ("Which of these artists is famous for cutting off his own ear? (a) Van Gogh (b) Picasso (c) Monet", "a", ["a", "b", "c"]),
        ("Who painted the Mona Lisa? (a) Da Vinci (b) Michelangelo (c) Rembrandt", "a", ["a", "b", "c"]),
        ("Which of these is a Baroque artist? (a) Raphael (b) Caravaggio (c) Botticelli", "b", ["a", "b", "c"]),
        ("Which of these artists is associated with the surrealist movement? (a) Dalí (b) Van Gogh (c) Pollock", "a", ["a", "b", "c"]),
        ("Which artist is known for the sculpture 'David'? (a) Michelangelo (b) Donatello (c) Bernini", "a", ["a", "b", "c"]),
        ("Which artist painted 'The Birth of Venus'? (a) Botticelli (b) Raphael (c) Titian", "a", ["a", "b", "c"]),
    ]
    for question, correct_answer, options in questions:
        response = ask_multiple_choice(question, correct_answer, options)
        if response == correct_answer:
            score += 1
            print("Correct!")
        else:
            print("Incorrect.")
        print(f"Your current score is: {score}")
    print("That's the end of our art adventure quiz!")
    print(f"Your final score is: {score}")
    return score

# Interests
def interests_of_autor():
    question = "Which of the following artists interest you the most? Please, choose at most three."
    options = [
        "ignacio-pinazo-camarlench", "fillol-granell-antonio", "federico-de-madrazo",
        "diego-rodriguez-de-silva-y-velazquez", "tiziano-vecellio", "joaquin-sorolla",
        "fiodor-rokotov", "peter-paul-rubens", "rembrandt-van-rijn", "pieter-bruegel-el-vell",
        "j-m-w-turner", "leonardo-da-vinci", "rosa-bonheur", "winslow-homer",
        "edouard-vuillard", "charles-burchfield", "ben-shahn", "sandro-botticelli",
        "salvador-dali", "edvard-munch", "edouard-manet", "hieronymus-bosch",
        "johannes-vermeer", "eugene-delacroix", "not-sure"
    ]
    return ask_multiple_options(question, options, 3)

def interests_of_style():
    question = "Which of the following styles interest you the most? Please, choose at most three."
    options = [
        "modernisme", "romanticisme", "barroc", "renaixement", "impressionisme",
        "realisme", "contemporani", "surrealisme", "expressionisme", "not-sure"
    ]
    return ask_multiple_options(question, options, 3)

# Función para reunir la información del visitante
def gather_visitor_info():
    print("Hello! My name is Muse, and I'm here to make your experience in the museum better.")
    print("In order to personalize your experience, I need you to answer a few questions.")
    print("It will only take a couple of minutes. Ready? Let's go!")

    first_visit = yes_or_no("Is this your first time visiting the museum (yes/no)? ")
    visitas = primera_visita(first_visit)  # Número de visitas previas
    companyia = amb_qui_vens()  # Compañía (solo, pareja, familia, grupo)
    dies = dies_visita()
    hores = hores_visita_per_dia()  # Horas por día
    edat = age_question(companyia) 
    estudis = studies()# Edad del visitante (o la más joven en el grupo)
    coneixement = art_knowledge()  # Conocimiento sobre arte
    quizz = start_quiz()  # Puntuación del quiz
    interessos_autor = interests_of_autor()  # Intereses en autores
    interessos_estils = interests_of_style()  # Intereses en estilos

    # Crear un objeto Visitant con los valores recolectados
    visitant = Visitant(
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

    return visitant


#Abstraccio

def classify_museum(number_visits):
    if number_visits < 2:
        category_museum = "Novice"
    elif 2 <= number_visits < 4:
        category_museum = "Beginner"
    elif 4 <= number_visits < 6:
        category_museum = "Intermediate"
    elif 6 <= number_visits < 8:
        category_museum = "Advanced"
    else:
        category_museum = "Expert"

    print("Thank you for completing the quiz! I hope you have enjoyed it.")
    print("I have been creating a gallery with all of the information you have provided me with.")
    print("Let's look into the conclusions I've gotten to.")
    print()
    print(f"Based on the times you've visited the museum, you are {category_museum}.")
    print()

    return category_museum


def classify_age(age):
    if age < 13:
        category_age = "Child"
    elif 13 <= age < 20:
        category_age = "Teenager"
    elif 20 <= age < 65:
        category_age = "Adult"
    else:
        category_age = "Senior"

    print(f"Based on your age, you are a {category_age}.")
    print()

    return category_age


def evaluate_knowledge(visitante):
    # Desglosar los datos del visitante
    age = visitante.edat
    studies = visitante.estudis
    art_knowledge = visitante.coneixements
    number_visits = visitante.visites
    quiz_score = visitante.quizz

    # Initialize scores
    study_score = 1 if studies == "yes" else 0
    age_score = age / 100  # Normalize age between 0 and 1
    knowledge_score = art_knowledge / 10  # Normalize art knowledge between 0 and 1
    number_visits_score = number_visits / 10
    score_test = quiz_score / 6  # Assume 6 questions in the quiz

    # Calculate total score
    total_score = (age_score * 0.05 +
                   number_visits_score * 0.1 +
                   study_score * 0.15 +
                   knowledge_score * 0.3 +
                   score_test * 0.4)

    # Determine category based on total score
    if total_score <= 0.2:
        category_knowledge = "Novice"
    elif total_score <= 0.4:
        category_knowledge = "Beginner"
    elif total_score <= 0.6:
        category_knowledge = "Intermediate"
    elif total_score <= 0.8:
        category_knowledge = "Advanced"
    else:
        category_knowledge = "Expert"

    total_score_rounded = round(total_score, 3)
    print(f"According to your art knowledge self-evaluation, quiz results, and art studies, "
          f"you are a {category_knowledge} with a score of {total_score_rounded}.")
    print()

    return category_knowledge, total_score_rounded

def show_visitor_classification(visitante):
    # Clasificación del museo según el número de visitas
    category_museum = classify_museum(visitante.visites)

    # Clasificación por edad
    category_age = classify_age(visitante.edat)

    # Evaluación del conocimiento sobre arte
    category_knowledge, total_score = evaluate_knowledge(visitante)

    # Mostrar todos los resultados juntos
    print("\n--- Final Results ---")
    print(f"Visitor's museum classification: {category_museum}")
    print(f"Visitor's age classification: {category_age}")
    print(f"Visitor's knowledge classification: {category_knowledge}")
    print(f"Total Knowledge Score: {total_score}")
    
    knowledge_factor = (
        1. if category_knowledge <= "Novice" else
        1.1 if category_knowledge <= "Beginner" else
        1.2 if category_knowledge <= "Intermediate" else
        1.3 if category_knowledge <= "Advanced" else
        1.4
    )
    return knowledge_factor
    
#Matching
def calculate_route_scores(visitant, category_museum, category_age, category_knowledge, rutes):
    
    scores = {}  # Diccionari per guardar les puntuacions de cada ruta

    # Ruta 1: Experiència baixa, ideal per a nens i novells
    scores['ruta1'] = 0
    if visitant.visites == 0:  # Primera visita
        scores['ruta1'] += 2
    if category_museum == "Novice":
        scores['ruta1'] += 2
    if category_age == "Child":
        scores['ruta1'] += 3
    if category_knowledge == "Novice":
        scores['ruta1'] += 2

    # Ruta 2: Experiència mitjana-baixa
    scores['ruta2'] = 0
    if category_museum in ["Beginner", "Intermediate"]:
        scores['ruta2'] += 2
    if category_knowledge in ["Beginner", "Intermediate"]:
        scores['ruta2'] += 2
    if visitant.dies > 1:  # Dies mitjans
        scores['ruta2'] += 2

    # Ruta 3: Experiència mitjana-alta, pensada per a joves amb cert coneixement
    scores['ruta3'] = 0
    if category_age == "Teenager":
        scores['ruta3'] += 3
    if visitant.coneixements == "yes":
        scores['ruta3'] += 2
    if visitant.visites >= 2:
        scores['ruta3'] += 2

    # Ruta 4: Experiència alta, ideal per a adults sols i coneixedors
    scores['ruta4'] = 0
    if visitant.companyia == "alone":
        scores['ruta4'] += 2
    if category_knowledge in ["Intermediate", "Advanced", "Expert"]:
        scores['ruta4'] += 3
    if any(style in ["modernisme", "barroc", "renaixement", "realisme"] for style in visitant.interessos_estils):
        scores['ruta4'] += 2

    # Ruta 5: Experiència baixa amb dies mitjans i nens
    scores['ruta5'] = 0
    if category_age == "Child":
        scores['ruta5'] += 3
    if visitant.dies > 1:
        scores['ruta5'] += 2
    if category_museum == "Novice":
        scores['ruta5'] += 2

    # Ruta 6: Experiència baixa sense nens amb dies mitjans
    scores['ruta6'] = 0
    if category_age in ["Adult", "Teenager"]:
        scores['ruta6'] += 2
    if visitant.dies == 2:
        scores['ruta6'] += 2
    if visitant.coneixements == "no":
        scores['ruta6'] += 2

    # Ruta 7: Experiència mitjana-baixa amb dies mitjans
    scores['ruta7'] = 0
    if visitant.companyia == "group":
        scores['ruta7'] += 2
    if category_age == "Teenager":
        scores['ruta7'] += 2
    if visitant.dies == 2:
        scores['ruta7'] += 2

    # Ruta 8: Experiència mitjana amb dies mitjans
    scores['ruta8'] = 0
    if category_age == "Senior":
        scores['ruta8'] += 2
    if category_knowledge in ["Intermediate", "Advanced"]:
        scores['ruta8'] += 2
    if visitant.visites >= 3:
        scores['ruta8'] += 2

    # Ruta 9: Experiència alta amb dies mitjans
    scores['ruta9'] = 0
    if visitant.companyia == "group":
        scores['ruta9'] += 3
    if visitant.dies >= 2:
        scores['ruta9'] += 2
    if category_knowledge in ["Advanced", "Expert"]:
        scores['ruta9'] += 3

    # Ruta 10: Experiència baixa amb dies alts i nens
    scores['ruta10'] = 0
    if category_age == "Child":
        scores['ruta10'] += 3
    if visitant.dies > 3:
        scores['ruta10'] += 2
    if visitant.visites == 0:
        scores['ruta10'] += 2

    # Ruta 11: Experiència baixa amb dies alts sense nens
    scores['ruta11'] = 0
    if category_age == "Adult":
        scores['ruta11'] += 2
    if visitant.dies > 3:
        scores['ruta11'] += 2

    # Ruta 12: Experiència mitjana-baixa amb dies alts
    scores['ruta12'] = 0
    if visitant.dies > 3:
        scores['ruta12'] += 3
    if visitant.coneixements == "yes":
        scores['ruta12'] += 2

    # Ruta 13: Experiència mitjana amb dies alts
    scores['ruta13'] = 0
    if category_knowledge in ["Intermediate", "Advanced"]:
        scores['ruta13'] += 3
    if visitant.dies > 3:
        scores['ruta13'] += 2

    # Ruta 14: Experiència alta amb moltes dies
    scores['ruta14'] = 0
    if category_knowledge in ["Advanced", "Expert"]:
        scores['ruta14'] += 3
    if visitant.dies > 4:
        scores['ruta14'] += 3
    if visitant.companyia == "alone":
        scores['ruta14'] += 2

    # Selecció final de la millor ruta
    final_route_name = max(scores, key=scores.get)
    print(f"La ruta recomanada segons les teves preferències és: {final_route_name}")

    for ruta in rutes:
        if ruta.nom == final_route_name:
            return ruta

# Función de integración con la clase Visitant y clasificaciones

def recommend_route(visitante, rutes):
    # Clasificar visitante según sus datos
    category_museum = classify_museum(visitante.visites)
    category_age = classify_age(visitante.edat)
    category_knowledge, _ = evaluate_knowledge(visitante)

    # Calcular puntajes de rutas
    final_route = calculate_route_scores(visitante, category_museum, category_age, category_knowledge, rutes)

    return final_route

#refinament
def calculate_observation_time(painting, knowledge_factor):
    complexity = painting.complexitat
    dim_cm2 = painting.dim_cm2
    relevance = painting.rellevancia
    
    
    base_time = 1.0 if dim_cm2 < 5007 else 2.0

    complexity_factor = (
        1.1 if complexity <= 1 else
        1.2 if complexity <= 2 else
        1.3 if complexity <= 3 else
        1.4 if complexity <= 4 else
        1.5
    )

    relevance_factor = (
        1.1 if relevance <= 1 else
        1.2 if relevance <= 2 else
        1.3 if relevance <= 3 else
        1.4 if relevance <= 4 else
        1.5
    )
    

    total_time = (base_time * complexity_factor * relevance_factor * knowledge_factor)
    return total_time


def add_paintings_to_route(route, new_paintings_by_style, new_paintings_by_author, visitant, knowledge_factor):
    max_time = visitant.hores * 60 * visitant.dies

    for painting in new_paintings_by_style:
        time_for_painting = calculate_observation_time(painting, knowledge_factor)
        if painting.name not in route.quadres and route.time + time_for_painting < max_time:
            route.quadres.append(painting.nom)
            route.time += time_for_painting

    for painting in new_paintings_by_author:
        time_for_painting = calculate_observation_time(painting, knowledge_factor)
        if painting.name not in route.quadres and route.author_intereststime + time_for_painting < max_time:
            route.quadres.append(painting.nom)
            route.time += time_for_painting


def remove_paintings_from_route(route, paintings_of_interest, visitant, quadres, knowledge_factor):
    max_time = visitant.hores * 60 * visitant.dies
    
    for painting in quadres:
        if route.temps > max_time and painting.nom not in paintings_of_interest and painting in route.quadres:
            time_for_painting = calculate_observation_time(painting, knowledge_factor)
            route.quadres.remove(painting.nom)
            route.temps -= time_for_painting



def fill_remaining_time(route, visitant, quadres, knowledge_factor):
    
    max_time = visitant.hores * 60 * visitant.dies
    
    for painting in quadres:
        if route.temps < max_time and painting.nom not in route.quadres:
            time_for_painting = calculate_observation_time(painting, knowledge_factor)
            route.quadres.append(painting.nom)
            route.temps += time_for_painting
    

def refine_route(route, visitante, all_paintings, knowledge_factor):
    """
    Refine the recommended route by adding or removing paintings based on visitor preferences and time constraints.
    """
    route.temps = route.temps * knowledge_factor
    # Find paintings by style and author interests
    paintings_by_style = [quadre.nom for quadre in all_paintings if quadre.estil==visitante.interessos_estils ]
    paintings_by_author = [quadre.nom for quadre in all_paintings if quadre.autor==visitante.interessos_autor ]

    # Add paintings to the route
    for ruta in rutes:
        if ruta.nom == route:
            add_paintings_to_route(
                ruta, paintings_by_style, paintings_by_author,
                visitante, knowledge_factor
            )

    # Remove paintings if the route exceeds time constraints
        if ruta.temps >= visitante.dies * visitante.hores *60:
            remove_paintings_from_route(
                ruta, paintings_by_style+ paintings_by_author,
                visitante, all_paintings, knowledge_factor
            )

        if ruta.temps < visitante.dies * visitante.hores *60:
            # Fill remaining time with other paintings
            fill_remaining_time(
                ruta, visitante, all_paintings, knowledge_factor
            )

#Print final


def show_paintings_by_rooms(ruta, sales, quadres, visitant, knowledge_factor):
    total_time_per_day = visitant.hores * 60 + (visitant.hores * 60 * 0.1) 
    day = 1
    remaining_time = total_time_per_day

    print(f"Details for {ruta}:")
    for room in sales:
        paintings_in_room = []

        for painting in quadres:
            room_of_painting = painting.sala

            if room == room_of_painting:
                time_for_painting = calculate_observation_time(painting, knowledge_factor)

                if time_for_painting > remaining_time:
                    if paintings_in_room:
                        print(f"Day {day}: The paintings to see in room {room} are:")
                        for p, t in paintings_in_room:
                            print(f"  - {p.autor}, time: {t:.2f} minutes")

                    print(f"Total time used on day {day}: {total_time_per_day - remaining_time:.2f} minutes\n")
                    paintings_in_room = [(painting, time_for_painting)]
                    day += 1

                    if day > visitant.dies:
                        #print("The route cannot fit into the available days.")
                        return

                    remaining_time = total_time_per_day - time_for_painting
                else:
                    paintings_in_room.append((painting, time_for_painting))
                    remaining_time -= time_for_painting

        if paintings_in_room:
            print(f"Day {day}: The paintings to see in room {room} are:")
            for p, t in paintings_in_room:
                print(f"  - {p.nom}, time: {t:.2f} minutes")

    print(f"Total time used on day {day}: {total_time_per_day - remaining_time:.2f} minutes\n")
    print(f"Total route time: {ruta.temps:.2f} minutes\n")

def puntuar_ruta():
    return ask_question_numerical("Puntua la ruta del 1-5? ", 1, 5)

#Init

if __name__ == "__main__":
    #file_path = "cuadros.txt"  # Cambia la ruta al archivo real
    #quadres, autores = parse_cuadros(file_path)
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
    # Asignar las salas según el estilo de cada cuadro
    #salas = assign_salas(quadres)
    rutes = rutes_predeterminades(quadres)
    visitante = gather_visitor_info()
    knowledge_factor = show_visitor_classification(visitante)
    ruta = recommend_route(visitante, rutes)
    refine_route(ruta, visitante, quadres, knowledge_factor)
    show_paintings_by_rooms(ruta, sales, quadres, visitante, knowledge_factor)
    puntuacio_ruta = puntuar_ruta()
