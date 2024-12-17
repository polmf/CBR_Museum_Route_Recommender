import streamlit as st
import json
from helpers.mapa_museu import mark_room_by_number, generate_museum_layout
import matplotlib.pyplot as plt

def render(routa):
    """Función para renderizar días, salas y cuadros usando Streamlit."""
    # print(routa)
    ruta_quadres = routa['ruta_quadres']
    
    # Es crea un conjunt de dies per escollir
    all_days = [item['day'] for item in ruta_quadres]
    selected_day = st.selectbox("Select the day", sorted(all_days))

    # Filtrar per dia seleccionat
    filtered_rutas = [
        item 
        for item in ruta_quadres
        if item["day"] == selected_day
    ]

    # Obtener una lista de salas únicas para el día seleccionado
    all_rooms = {
        room  # Solo agregar las claves de 'rooms', que son los nombres de las salas
        for item in filtered_rutas
        for room in item['rooms'].keys()  # Obtener las claves (nombres de salas)
    }

    selected_room = st.selectbox("Select the room", sorted(all_rooms))

    
    # Mostrar los cuadros en la sala seleccionada
    st.header(f"Day: {selected_day}")
    st.subheader(f"Room: {selected_room}")

    # Mostrar mapa con la sala seleccionada
    MUSEU_LAYOUT = generate_museum_layout()
    fig = mark_room_by_number(int(selected_room.split()[1]), MUSEU_LAYOUT)  # Extraer el número de la sala
    st.pyplot(fig)  # Renderizar el mapa con la sala seleccionada

    # Filtrar y mostrar cuadros
    for entry in filtered_rutas:
        for room_name, room_data in entry["rooms"].items():  # Accedemos a las claves y valores del diccionario 'rooms'
            if room_name == selected_room:  # Comparamos el nombre de la sala
                # Extraemos solo los nombres de los cuadros de las sublistas
                paintings = [painting[0] for painting in room_data]
                links = [painting[1] for painting in room_data]  # Obtenemos los enlaces de las imágenes
                minuts = [painting[2] for painting in room_data]

                # Mostrar los cuadros uno debajo del otro con enlaces para ver la imagen
                for painting, minuts, link in zip(paintings, minuts, links):
                    st.write(f"{painting} - {minuts} min - [See image]({link})")
