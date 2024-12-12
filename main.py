import streamlit as st
from helpers.database import load_database
from pages.general_info import render as general_info
from pages.personal_bg import render as personal_bg
from pages.art_quiz import render as art_quiz
from pages.interests import render as interests

# Inicializar paso actual si no existe
if "step" not in st.session_state:
    st.session_state.step = 0

# Funciones para manejar cambios de paso
def go_next():
    st.session_state.step += 1

def go_back():
    st.session_state.step -= 1

# Cargar datos necesarios
df = load_database()

# Layout para evitar la barra lateral
#st.set_page_config(layout="wide")

# Control de flujo continuo basado en `st.session_state.step`
def render_page():
    step = st.session_state.step

    if step == 0:
        general_info(df)  # Página 1: General Information
        st.button("Next", on_click=go_next)
    elif step == 1:
        personal_bg()  # Página 2: Personal Background
        col1, col2 = st.columns(2)
        with col1:
            st.button("Back", on_click=go_back)
        with col2:
            st.button("Next", on_click=go_next)
    elif step == 2:
        art_quiz()  # Página 3: Art Quiz
        col1, col2 = st.columns(2)
        with col1:
            st.button("Back", on_click=go_back)
        with col2:
            st.button("Next", on_click=go_next)
    elif step == 3:
        interests(df)  # Página 4: Interests
        col1, col2 = st.columns(2)
        with col1:
            st.button("Back", on_click=go_back)
        with col2:
            st.button("Next", on_click=go_next)
    elif step == 4:
        st.write("Recommended Route Page")  # Aquí puedes añadir la lógica de la última página
        st.button("Back", on_click=go_back)

# Asegurarse de renderizar la página correcta
render_page()