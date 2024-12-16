import streamlit as st
import random
from generacio.recom_clips import Ruta
from generacio.recom_clips import show_paintings_by_rooms_sense_prints as reestructura_ruta
from generacio.classes import Visitant
from blocs.general_info import render as general_info
from blocs.personal_bg import render as personal_bg
from blocs.art_quiz import render as art_quiz
from blocs.interests import render as interests
from blocs.rutes_proposades import render as rutes_recomenades
from blocs.detalls_ruta import render as detalls_ruta
from helpers.database import load_database
from helpers.mapa_museu import fer_rutes
from helpers.cbr_process import cbr_recuperar_reutilizar as cbr_1
from helpers.cbr_process import cbr_revisar_retener as cbr_2

informative_phrases = [
    "Creating your recommended museum routes... Hold tight!",
    "Compiling the best museum tours just for you...",
    "Crafting the perfect route... Almost there!",
    "Organizing your museum journey... One moment!"
]

# Lista de frases divertidas o bromas para el usuario
funny_phrases = [
    "Don’t worry, the museum isn’t going anywhere! 😄",
    "Meanwhile, we are finding the best route, don’t take a nap! 😉",
    "Just a few more seconds... Try not to get lost in thought! 😜",
    "It’s loading, but you can already start planning your future museum selfies! 😎"
]

# Función para mostrar las dos frases: una informativa y una divertida
def display_funny_and_informative_messages():
    # Elegir una frase aleatoria de cada grupo
    informative_message = random.choice(informative_phrases)
    funny_message = random.choice(funny_phrases)
    
    st.write(informative_message)  # Mostrar frase informativa
    st.write(funny_message)        # Mostrar frase divertida

# Inicializar paso actual si no existe
if "step" not in st.session_state:
    st.session_state.step = 0

# Funciones para manejar cambios de paso
def go_next():
    st.session_state.step += 1
  
def go_next_d1():
    st.session_state.druta = st.session_state.rutes_recomenades_reconstrudides[0]
    st.session_state.step += 1

def go_next_d2():
    st.session_state.druta = st.session_state.rutes_recomenades_reconstrudides[1]
    st.session_state.step += 1

def go_next_d3():
    st.session_state.druta = st.session_state.rutes_recomenades_reconstrudides[2]
    st.session_state.step += 1
    
def go_next_1():
    st.session_state.ruta = 1
    st.session_state.ruta_completa = st.session_state.rutes_recomenades_reconstrudides[0]
    st.session_state.step += 2

def go_next_2():
    st.session_state.ruta = 2
    st.session_state.ruta_completa = st.session_state.rutes_recomenades_reconstrudides[1]
    st.session_state.step += 2

def go_next_3():
    st.session_state.ruta = 3
    st.session_state.ruta_completa = st.session_state.rutes_recomenades_reconstrudides[2]
    st.session_state.step += 2

def go_final(evaluation):
    st.session_state.evaluation = evaluation
    st.success("Thank you for rating!")
    st.session_state.step += 1

def go_back():
    st.session_state.step -= 1

# Función para manejar la selección de la ruta
def seleccionar_ruta(ruta):
    st.session_state.ruta = ruta  # Guardar la ruta seleccionada

# Cargar datos necesarios
df = load_database()

# Control de flujo continuo basado en st.session_state.step
def render_page():
    step = st.session_state.step

    # Crear un espacio vacío para limpiar elementos anteriores
    empty = st.empty()

    if step == 0:
        general_info()  # Página 1: General Information
        col1, col2, col3 = st.columns(3)
        with col3:
            st.button("Next", on_click=go_next)
    elif step == 1:
        personal_bg()  # Página 2: Personal Background
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("Back", on_click=go_back)
        with col3:
            st.button("Next", on_click=go_next)
    elif step == 2:
        art_quiz()  # Página 3: Art Quiz
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("Back", on_click=go_back)
        with col3:
            st.button("Next", on_click=go_next)
    elif step == 3:
        interests(df)  # Página 4: Interests
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("Back", on_click=go_back)
        with col3:
            st.button("Finish", on_click=go_next)
    elif step == 4:
        # Limpiar la pantalla de la página anterior
        st.session_state.user_to_recommend = Visitant(
            visites=st.session_state.visitas,
            companyia=st.session_state.companyia,
            dies=st.session_state.dies,
            hores=st.session_state.hores,
            edat=st.session_state.edat,
            estudis=st.session_state.estudis,
            coneixement=st.session_state.coneixement,
            quizz=st.session_state.score,
            interessos_autor=st.session_state.interessos_autor,
            interessos_estils=st.session_state.interessos_estils,
            interessos_tipus=st.session_state.interessos_tipus
        )
        
        # Mostrar el encabezado
        st.header("Making Routes")
        
        # Mostrar las dos frases: una informativa y una divertida
        display_funny_and_informative_messages()
        
        # Crear un contenedor vacío para centrar el spinner y el botón
        with st.spinner('Loading...'):
            # Asegúrate de que el spinner se muestra mientras se ejecuta la función
            st.session_state.rutes_recomenades, st.session_state.most_similar_cluster = cbr_1()
            
            st.session_state.rutes_recomenades_reconstrudides = []
            for ruta in st.session_state.rutes_recomenades:
                ruta_nova = Ruta(nom='Ruta_nova', instancies=ruta['instancies'])
                ruta_restructurada = reestructura_ruta(ruta_nova, st.session_state.user_to_recommend, (1 + 0.04 * (st.session_state.coneixement - 1)))
                
                ruta_new = {}
                ruta_new['ruta_quadres'] = ruta_restructurada
                ruta_new['quadres'] = ruta['quadres']
                ruta_new['temps'] = ruta['temps']
                ruta_new['puntuacio'] = ruta['puntuacio']
                ruta_new['ruta'] = ruta['ruta']
                
                st.session_state.rutes_recomenades_reconstrudides.append(ruta_new)

            fer_rutes(st.session_state.rutes_recomenades_reconstrudides)  # Llamada a tu función"""
            # print('rutes recom recons: ', st.session_state.rutes_recomenades_reconstrudides)
        
        # Crear columnas para centrar el botón
        col1, col2, col3 = st.columns([1, 4, 1])  # 4 es el ancho de la columna central
        with col2:
            # Este botón se centra en la columna 2
            st.button("View Recommended Routes", on_click=go_next)
            
    elif step == 5:
        # Paso 4: Selección de la ruta
        st.header("Elige tu ruta")
        # Mostrar botones para seleccionar las rutas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("Detalles Ruta 1", on_click=go_next_d1)  # Guardar ruta seleccionada
        with col2:
            st.button("Detalles Ruta 2", on_click=go_next_d2)  # Guardar ruta seleccionada
        with col3:
            st.button("Detalles Ruta 3", on_click=go_next_d3)
        
        rutes_recomenades()  # Llamamos la función que renderiza las rutas

        with col1:
            st.button("Ruta 1", on_click=go_next_1)  # Guardar ruta seleccionada
        with col2:
            st.button("Ruta 2", on_click=go_next_2)  # Guardar ruta seleccionada
        with col3:
            st.button("Ruta 3", on_click=go_next_3)  # Guardar ruta seleccionada

    elif step == 6:
        
        detalls_ruta(st.session_state.druta)

        # Paso 5: Mostrar la ruta seleccionada
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("Back", on_click=go_back)
        
    elif step == 7:
        if st.session_state.ruta:
            # Mostrar la ruta seleccionada
            st.write(f"Ruta seleccionada: {st.session_state.ruta}")
            # Llamamos a la función render de route_page.py para mostrar la ruta seleccionada
            detalls_ruta(st.session_state.ruta_completa)
            col1, col2, col3 = st.columns(3)
            with col3:
                st.button("Finish", on_click=go_next)
    elif step == 8:
        st.header("Route Evaluation")
        # Allow the user to rate the selected route from 1 to 5
        evaluation = st.slider("Rate the selected route (1: Very bad, 5: Excellent):", 1, 5, 3)
        st.button("Submit Rating", on_click=go_final(evaluation))
        
    elif step == 9:
        cbr_2()
        st.header("Goodbye!")
        st.write("Thank you for exploring the museum with us! We hope you enjoyed your experience.")
        st.write("Feel free to come back anytime.")
# Asegurarse de renderizar la página correcta
render_page()