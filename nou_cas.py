import streamlit as st
import base64

# Función para cargar la imagen y convertirla a Base64
def set_background(image_file):
    # Leer la imagen local
    with open(image_file, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode()
    # Crear el CSS para el fondo
    css_code = f"""
    <style>
    body {{
        background-image: url("data:image/png;base64,{base64_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)

# Cambiar la ruta al archivo local según corresponda
set_background("fondo.jpg")

# Funciones de preguntas
def ask_yes_or_no(question):
    return st.radio(question, options=["Yes", "No"]) == "Yes"

def ask_question_numerical(question, min_value, max_value):
    return st.slider(question, min_value=min_value, max_value=max_value)

def ask_question(question, options):
    return st.radio(question, options=options)

def ask_multiple_options(question, options, limit):
    selected = st.multiselect(question, options=options)
    if len(selected) > limit:
        st.warning(f"You can select up to {limit} options.")
    return selected[:limit]

# Función principal para los bloques
def main():
    st.title("Museum Visitor Questionnaire")

    # Estado inicial
    if "block" not in st.session_state:
        st.session_state.block = 1  # Comenzar en el bloque 1

    # Bloque 1: General Information
    if st.session_state.block == 1:
        st.header("Block 1: General Information")
        first_visit = ask_yes_or_no("Is this your first time visiting the museum?")
        visitas = 0 if first_visit else ask_question_numerical("How many times have you been here before?", 1, 10)
        companyia = ask_question("Who are you visiting the museum with?", ["Alone", "Couple", "Family", "Group"])
        dies = ask_question_numerical("How many days are you planning on coming to the museum?", 1, 10)
        hores = ask_question_numerical("How many hours do you want to spend each day?", 1, 12)

        if st.button("Next"):
            # Guardar respuestas en estado
            st.session_state.first_visit = first_visit
            st.session_state.visitas = visitas
            st.session_state.companyia = companyia
            st.session_state.dies = dies
            st.session_state.hores = hores
            st.session_state.block = 2  # Ir al siguiente bloque

    # Bloque 2: Personal Background
    elif st.session_state.block == 2:
        st.header("Block 2: Personal Background")
        edat = ask_question_numerical(
            f"How old are {'you' if st.session_state.companyia == 'Alone' else 'the youngest in the group'}?",
            0,
            110,
        )
        estudis = ask_yes_or_no("Have you studied any art-related subjects?")
        coneixement = ask_question_numerical("On a scale from 1 to 10, how would you rate your art knowledge?", 1, 10)

        if st.button("Next"):
            # Guardar respuestas en estado
            st.session_state.edat = edat
            st.session_state.estudis = estudis
            st.session_state.coneixement = coneixement
            st.session_state.block = 3  # Ir al siguiente bloque

    # Bloque 3: Art Quiz
    elif st.session_state.block == 3:
        st.header("Block 3: Art Quiz")
        st.write("Let's test your art knowledge with a quick quiz!")
        questions = [
            ("Which artist cut off his own ear?", "Van Gogh", ["Van Gogh", "Picasso", "Monet"]),
            ("Who painted the Mona Lisa?", "Da Vinci", ["Da Vinci", "Michelangelo", "Rembrandt"]),
            ("Which is a Baroque artist?", "Caravaggio", ["Raphael", "Caravaggio", "Botticelli"]),
            ("Which of these artists is associated with the surrealist movement?", "Dalí", ["Dalí", "Van Gogh", "Pollock"]),
            ("Which artist is known for the sculpture 'David'?", "Michelangelo", ["Michelangelo", "Donatello", "Bernini"]),
            ("Which artist painted 'The Birth of Venus'?", "Botticelli", ["Botticelli", "Raphael", "Titian"]),
        ]
        score = 0
        for question, correct_answer, options in questions:
            answer = st.radio(question, options=options, key=question)  # Key único por pregunta
            if answer == correct_answer:
                score += 1

        if st.button("Next"):
            st.session_state.score = score
            st.session_state.block = 4  # Ir al siguiente bloque

    # Bloque 4: Interests
    elif st.session_state.block == 4:
        st.header("Block 4: Interests")
        interessos_autor = ask_multiple_options(
            "Which artists interest you the most? (Choose up to 3)",
            [
                "ignacio-pinazo-camarlench", "fillol-granell-antonio", "federico-de-madrazo",
                "diego-rodriguez-de-silva-y-velazquez", "tiziano-vecellio", "joaquin-sorolla",
                "fiodor-rokotov", "peter-paul-rubens", "rembrandt-van-rijn", "pieter-bruegel-el-vell",
                "j-m-w-turner", "leonardo-da-vinci", "rosa-bonheur", "winslow-homer",
                "edouard-vuillard", "charles-burchfield", "ben-shahn", "sandro-botticelli",
                "salvador-dali", "edvard-munch", "edouard-manet", "hieronymus-bosch",
                "johannes-vermeer", "eugene-delacroix", "not-sure"
            ],
            3,
        )
        interessos_estils = ask_multiple_options(
            "Which styles interest you the most? (Choose up to 3)",
            [
                "modernisme", "romanticisme", "barroc", "renaixement", "impressionisme",
                "realisme", "contemporani", "surrealisme", "expressionisme", "not-sure"
            ],
            3,
        )

        if st.button("Finish"):
            # Guardar respuestas en estado
            st.session_state.interessos_autor = interessos_autor
            st.session_state.interessos_estils = interessos_estils
            st.session_state.block = 5  # Ir al resumen

    # Resumen final
    elif st.session_state.block == 5:
        st.header("Summary of Your Answers")
        st.write({
            "First Visit": st.session_state.first_visit,
            "Previous Visits": st.session_state.visitas,
            "Companionship": st.session_state.companyia,
            "Days Planned": st.session_state.dies,
            "Hours per Day": st.session_state.hores,
            "Age": st.session_state.edat,
            "Art Studies": st.session_state.estudis,
            "Art Knowledge": st.session_state.coneixement,
            "Quiz Score": st.session_state.score,
            "Interested Artists": st.session_state.interessos_autor,
            "Interested Styles": st.session_state.interessos_estils,
        })

        if st.button("Restart"):
            st.session_state.block = 1  # Reiniciar cuestionario

if __name__ == "__main__":
    main()
