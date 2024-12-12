import streamlit as st

def render():
    st.header("Art Quiz")
    questions = [
            ("Which artist cut off his own ear?", "Van Gogh", ["Van Gogh", "Picasso", "Monet"]),
            ("Who painted the Mona Lisa?", "Da Vinci", ["Da Vinci", "Michelangelo", "Rembrandt"]),
            ("Which is a Baroque artist?", "Caravaggio", ["Raphael", "Caravaggio", "Botticelli"]),
            ("Which of these artists is associated with the surrealist movement?", "Dalí", ["Dalí", "Van Gogh", "Pollock"]),
            ("Which artist is known for the sculpture 'David'?", "Michelangelo", ["Michelangelo", "Donatello", "Bernini"]),
            ("Which artist painted 'The Birth of Venus'?", "Botticelli", ["Botticelli", "Raphael", "Titian"]),
        ]

    st.session_state.score = 0
    for question, correct_answer, options in questions:
        answer = st.radio(question, options, key=question)
        if answer == correct_answer:
            st.session_state.score += 1
