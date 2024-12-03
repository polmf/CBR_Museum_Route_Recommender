import streamlit as st
from ui_questions import ask_yes_or_no, ask_question_numerical, ask_question, ask_multiple_options
from cbr_process import handle_cbr_process

def render_block(block):
    if block == 1:
        st.header("Block 1: General Information")
        first_visit = ask_yes_or_no("Is this your first time visiting the museum?")
        visitas = 0 if first_visit else ask_question_numerical("How many times have you been here before?", 1, 10)
        companyia = ask_question("Who are you visiting the museum with?", ["Alone", "Couple", "Family", "Group"])
        dies = ask_question_numerical("How many days are you planning on coming to the museum?", 1, 10)
        hores = ask_question_numerical("How many hours do you want to spend each day?", 1, 12)

        col1, col2 = st.columns([1, 3])
        with col1:
            st.empty()

        with col2:
            if st.button("Next", key="block1_next"):
                st.session_state.first_visit = first_visit
                st.session_state.visitas = visitas
                st.session_state.companyia = companyia
                st.session_state.dies = dies
                st.session_state.hores = hores
                st.session_state.block = 2

    elif block == 2:
        st.header("Block 2: Personal Background")
        edat = ask_question_numerical(
            f"How old are {'you' if st.session_state.companyia == 'Alone' else 'the youngest in the group'}?",
            0,
            110
        )
        estudis = ask_yes_or_no("Have you studied any art-related subjects?")
        coneixement = ask_question_numerical("On a scale from 1 to 10, how would you rate your art knowledge?", 1, 10)

        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Back", key="block2_back"):
                st.session_state.block = 1
        with col2:
            if st.button("Next", key="block2_next"):
                st.session_state.edat = edat
                st.session_state.estudis = estudis
                st.session_state.coneixement = coneixement
                st.session_state.block = 3

    elif block == 3:
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
            answer = st.radio(question, options=options, key=question)
            if answer == correct_answer:
                score += 1

        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Back", key="block3_back"):
                st.session_state.block = 2
        with col2:
            if st.button("Next", key="block3_next"):
                st.session_state.score = score
                st.session_state.block = 4

    elif block == 4:
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
            3
        )

        interessos_estils = ask_multiple_options(
            "Which styles interest you the most? (Choose up to 3)",
            [
                "modernisme", "romanticisme", "barroc", "renaixement", "impressionisme",
                "realisme", "contemporani", "surrealisme", "expressionisme", "not-sure"
            ],
            3
        )

        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Back", key="block4_back"):
                st.session_state.block = 3
        with col2:
            if len(interessos_autor) <= 3 and len(interessos_estils) <= 3:
                if st.button("Finish", key="block4_finish"):
                    st.session_state.interessos_autor = interessos_autor
                    st.session_state.interessos_estils = interessos_estils
                    st.session_state.block = 5
            else:
                st.warning("Please select up to 3 interests in each category.")

    elif block == 5:
        st.header("Your Recommended Route")
        handle_cbr_process()

        if "ruta" in st.session_state:
            st.write("Aquí tienes la ruta recomendada para ti:")
            st.write(st.session_state.ruta)
            feedback = st.slider("Introduce una puntuación del 1 al 5 a la ruta recomendada", 1, 5)
            if st.button("Enviar Feedback"):
                from cbr_process import Retener
                retener = Retener(st.session_state.user_to_recommend, feedback)
                st.success("¡Gracias por tu feedback! Se ha registrado correctamente.")
        else:
            st.write("No hay ruta recomendada disponible.")