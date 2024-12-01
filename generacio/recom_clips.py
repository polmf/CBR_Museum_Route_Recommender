from classes import Visitant
from generacio_instancies import *

class Ruta:
    def __init__(self, nom, quadres, temps=0.0):
        self.nom = nom
        self.quadres = quadres
        self.temps = temps

    def get_nom(self):
        return self.nom
    
    def get_quadres(self):
        return self.quadres
    
    def get_temps(self):
        return self.temps

rutes = [
    Ruta(
        nom="ruta1",
        quadres=["The_Horse_Fair", "Un_monaguillo_solfeando", "Adoración_de_los_Reyes_Magos", "La_Mona_Lisa"],
    ),
    Ruta(
        nom="ruta2",
        quadres=[
            "Samson_and_Delilah", "Sol_de_sequía_en_julio", "The_Virgin_of_the_Rocks", "Orión_en_invierno",
            "City_of_the_Future", "Abstract_Minds", "Celestial_Explorations", "La_Virgen_con_el_Niño",
            "Retrato_de_Antonio_Anselmi", "Identidad"
        ],
    ),
    Ruta(
        nom="ruta3",
        quadres=[
            "Retrato_de_Antonio_Anselmi", "El_jardi_de_les_delicies", "La_zarina_Catalina_II",
            "Self_Portrait_at_the_Age_of_34"
        ],
    ),
    Ruta(
        nom="ruta4",
        quadres=[
            "Un_monaguillo_solfeando", "Autorretrato", "El_Gran_Capitán,_recorriendo_el_campo_de_la_batalla_de_Ceriñola",
            "El_pintor_Carlos_Luis_de_Ribera", "Francisco_Pacheco", "La_Virgen_con_el_Niño"
        ],
    ),
    Ruta(
        nom="ruta5",
        quadres=[
            "Abstract_Minds", "City_of_the_Future", "Celestial_Explorations", "Symphony_of_Lights",
            "Digital_Rebirth", "Identidad", "Orión_en_invierno", "La_zarina_Catalina_II"
        ],
    ),
    Ruta(
        nom="ruta6",
        quadres=[
            "The_Horse_Fair", "Samson_and_Delilah", "El_naixement_de_Venus", "Self_Portrait_at_the_Age_of_34",
            "Symphony_of_Lights", "Digital_Rebirth"
        ],
    ),
    Ruta(
        nom="ruta7",
        quadres=[
            "La_Mona_Lisa", "Adoración_de_los_Reyes_Magos", "La_ronda_de_nit", "Celestial_Explorations"
        ],
    ),
    Ruta(
        nom="ruta8",
        quadres=[
            "The_Virgin_of_the_Rocks", "The_Horse_Fair", "Sol_de_sequía_en_julio", "Ciervo_en_los_montes_Adirondacks",
            "La_cantante", "Orión_en_invierno"
        ],
    ),
    Ruta(
        nom="ruta9",
        quadres=[
            "Symphony_of_Lights", "Celestial_Explorations", "Digital_Rebirth", "Samson_and_Delilah",
            "La_Mona_Lisa", "Adoración_de_los_Reyes_Magos", "La_ronda_de_nit", "Celestial_Explorations"
        ],
    ),
]

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
    return ask_question("Who are you visiting the museum with? (alone/group) ", ["alone", "couple", "family", "group"])

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
    
#Matching
def calculate_route_scores(visitante, category_museum, category_age, category_knowledge, rutes):
    scores = {}

    # Ruta 1
    scores['ruta1'] = 0
    if visitante.visites == 0:  # Primera visita
        scores['ruta1'] += 1
    if category_museum == "Novice":
        scores['ruta1'] += 1
    if category_knowledge == "Novice":
        scores['ruta1'] += 1
    if visitante.coneixements == "no":
        scores['ruta1'] += 1
    if category_age == "Child":
        scores['ruta1'] += 1

    # Ruta 2
    scores['ruta2'] = 0
    if category_museum in ["Intermediate", "Beginner"]:
        scores['ruta2'] += 1
    if category_knowledge in ["Beginner", "Intermediate", "Advanced"]:
        scores['ruta2'] += 2
    if visitante.dies > 1:
        scores['ruta2'] += 2

    # Ruta 3
    scores['ruta3'] = 0
    if category_age == "Teenager":
        scores['ruta3'] += 1
    if visitante.coneixements == "yes":
        scores['ruta3'] += 2
    if visitante.visites >= 2:
        scores['ruta3'] += 2

    # Ruta 4
    scores['ruta4'] = 0
    if visitante.companyia == "alone":
        scores['ruta4'] += 1
    if category_knowledge in ["Intermediate", "Advanced"]:
        scores['ruta4'] += 2
    if any(style in ["modernisme", "romanticisme", "barroc", "renaixement", "realisme"] for style in visitante.interessos_estils):
        scores['ruta4'] += 2

    # Ruta 5
    scores['ruta5'] = 0
    if category_age == "Adult":
        scores['ruta5'] += 1
    if visitante.visites >= 3:
        scores['ruta5'] += 1
    if category_knowledge == "Expert":
        scores['ruta5'] += 2
    if visitante.companyia == "group":
        scores['ruta5'] += 1

    # Ruta 6
    scores['ruta6'] = 0
    if visitante.coneixements == "yes":
        scores['ruta6'] += 2
    if category_knowledge in ["Advanced", "Expert"]:
        scores['ruta6'] += 2
    if visitante.dies == 1:
        scores['ruta6'] += 1

    # Ruta 7
    scores['ruta7'] = 0
    if visitante.companyia == "group":
        scores['ruta7'] += 2
    if category_age == "Teenager":
        scores['ruta7'] += 2
    if visitante.dies == 1:
        scores['ruta7'] += 1

    # Ruta 8
    scores['ruta8'] = 0
    if category_age == "Senior":
        scores['ruta8'] += 2
    if category_knowledge in ["Intermediate", "Advanced"]:
        scores['ruta8'] += 2
    if visitante.visites >= 2:
        scores['ruta8'] += 1

    # Ruta 9
    scores['ruta9'] = 0
    if visitante.companyia == "group":
        scores['ruta9'] += 2
    if category_age == "Teenager":
        scores['ruta9'] += 2
    if visitante.dies > 1:
        scores['ruta9'] += 1

    # Selección final
    final_route = max(scores, key=scores.get)
    print(f"Based on your preferences and characteristics, the recommended route is: {final_route}")
    for ruta in rutes:
        if ruta.nom == final_route:
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
def calculate_observation_time(painting):
    complexity = painting.complexitat
    height = painting.alçada
    width = painting.amplada
    relevance = painting.rellevancia

    area = height * width
    base_time = 4.0 if area < 2500 else 8.0

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

    total_time = base_time * complexity_factor * relevance_factor
    return total_time


def add_paintings_to_route(route, new_paintings_by_style, new_paintings_by_author, visitant):
    max_time = visitant.hores * 60 * visitant.dies

    for painting in new_paintings_by_style:
        time_for_painting = calculate_observation_time(painting)
        if painting not in route.quadres and route.time + time_for_painting < max_time:
            route.quadres.append(painting)
            route.time += time_for_painting

    for painting in new_paintings_by_author:
        time_for_painting = calculate_observation_time(painting)
        if painting not in route.quadres and route.author_intereststime + time_for_painting < max_time:
            route.quadres.append(painting)
            route.time += time_for_painting


def remove_paintings_from_route(route, paintings_of_interest, visitant, quadres):
    max_time = visitant.hores * 60 * visitant.dies
    
    for painting in quadres:
        if route.temps > max_time and painting not in paintings_of_interest and painting in route.quadres:
            time_for_painting = calculate_observation_time(painting)
            route.quadres.remove(painting)
            route.temps -= time_for_painting



def fill_remaining_time(route, visitant, quadres):
    
    max_time = visitant.hores * 60 * visitant.dies
    
    for painting in quadres:
        if route.temps < max_time:
            time_for_painting = calculate_observation_time(painting)
            route.quadres.append(painting)
            route.temps += time_for_painting
    

def refine_route(route, visitante, all_paintings):
    """
    Refine the recommended route by adding or removing paintings based on visitor preferences and time constraints.
    """

    # Find paintings by style and author interests
    paintings_by_style = [quadre.nom for quadre in all_paintings if quadre.estil==visitante.interessos_estils ]
    paintings_by_author = [quadre.nom for quadre in all_paintings if quadre.autor==visitante.interessos_autor ]

    # Add paintings to the route
    for ruta in rutes:
        if ruta.nom == route:
            add_paintings_to_route(
                ruta, paintings_by_style, paintings_by_author,
                visitante
            )

    # Remove paintings if the route exceeds time constraints
        if ruta.temps >= visitante.dies * visitante.hores *60:
            remove_paintings_from_route(
                ruta, paintings_by_style+ paintings_by_author,
                visitante, all_paintings
            )

        if ruta.temps < visitante.dies * visitante.hores *60:
            # Fill remaining time with other paintings
            fill_remaining_time(
                ruta, visitante, all_paintings
            )

#Print final


def show_paintings_by_rooms(ruta, sales, quadres, visitant):
    total_time_per_day = visitant.hores * 60 + (visitant.hores * 60 * 0.1) 
    day = 1
    remaining_time = total_time_per_day

    print(f"Details for {ruta}:")
    for room in sales:
        paintings_in_room = []

        for painting in quadres:
            room_of_painting = painting.sala

            if room == room_of_painting:
                time_for_painting = calculate_observation_time(painting)

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
    file_path = "cuadros.txt"  # Cambia la ruta al archivo real
    quadres, autores = parse_cuadros(file_path)

    # Asignar las salas según el estilo de cada cuadro
    salas = assign_salas(quadres)
    visitante = gather_visitor_info()
    show_visitor_classification(visitante)
    ruta = recommend_route(visitante, rutes)
    refine_route(ruta, visitante, quadres)
    show_paintings_by_rooms(ruta, salas, quadres, visitante)
    puntuacio_ruta = puntuar_ruta()
