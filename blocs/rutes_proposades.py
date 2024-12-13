import streamlit as st
import os

# Directorio donde se encuentran los videos (ya convertidos de GIFs)
output_dir = os.path.join(os.getcwd(), "museum_videos")  # Aseguramos que el directorio es accesible

# Función para mostrar los detalles de cada ruta
def mostrar_detalles_ruta(ruta):
    if ruta == 1:
        st.write("Detalles de la Ruta 1:")
    elif ruta == 2:
        st.write("Detalles de la Ruta 2:")
    elif ruta == 3:
        st.write("Detalles de la Ruta 3:")

# Función para mostrar los videos de las tres rutas basados en el día
def mostrar_videos(dia):
    # Generar el nombre de los videos basándonos en el día
    rutas = [1, 2, 3]
    col1, col2, col3 = st.columns(3)  # Crear 3 columnas

    # Iterar sobre las rutas y mostrar el video en la columna correspondiente
    for idx, ruta in enumerate(rutas):
        video_path = os.path.join(output_dir, f"museum_route_{ruta}_day_{dia}.mp4")  # Formato de video .mp4
        
        with [col1, col2, col3][idx]:
            # Botón para mostrar los detalles de la ruta
            if st.button(f"Ver detalles Ruta {ruta}"):
                mostrar_detalles_ruta(ruta)  # Mostrar detalles de la ruta cuando se presiona el botón
                
            # Verificar si el archivo existe y mostrarlo
            if os.path.exists(video_path):
                st.subheader(f"Ruta {ruta}")
                st.video(video_path, format="video/mp4")
            else:
                # Si el video no existe, mostrar un mensaje de error en la columna correspondiente
                st.error(f"El archivo para Ruta {ruta} no existe. Verifica que el archivo de video esté en el directorio correcto.")

# Función para renderizar la página con los videos de las tres rutas
def render():
    # Día seleccionado
    dia = st.slider("Selecciona el día", min_value=1, max_value=5, step=1, value=1)
    
    # Llamamos a la función que muestra los videos de las tres rutas
    mostrar_videos(dia)