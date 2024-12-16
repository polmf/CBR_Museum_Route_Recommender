import streamlit as st
import json
from helpers.mapa_museu import mark_room_by_number, generate_museum_layout
import matplotlib.pyplot as plt

def render(routa):
    """Función para renderizar días, salas y cuadros usando Streamlit."""
    print(routa)
    # Es crea un conjunt de dies per escollir
    """rutes_recomanades_total = [
        {
            "ruta_quadres": [
                {
                    "day": entry["day"],
                    "rooms": [
                        {"room": room, "paintings": paintings}
                        for room, paintings in entry["rooms"].items()
                    ],
                }
                for entry in item['ruta_quadres']
            ]
        }
        for item in routa if 'ruta_quadres' in item
    ]"""
    
    # Es crea un conjunt de dies per escollir
    all_days = [item['day'] for item in routa]
    selected_day = st.selectbox("Selecciona el día", sorted(all_days))

    # Filtrar per dia seleccionat
    filtered_rutas = [
        item 
        for item in routa
        if item["day"] == selected_day
    ]

    # Obtener una lista de salas únicas para el día seleccionado
    all_rooms = {
        room  # Solo agregar las claves de 'rooms', que son los nombres de las salas
        for item in filtered_rutas
        for room in item['rooms'].keys()  # Obtener las claves (nombres de salas)
    }

    selected_room = st.selectbox("Selecciona la sala", sorted(all_rooms))

    # Mostrar los cuadros en la sala seleccionada
    st.header(f"Día: {selected_day}")
    st.subheader(f"Sala: {selected_room}")

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

                # Mostrar los cuadros uno debajo del otro con enlaces para ver la imagen
                for painting, link in zip(paintings, links):
                    st.write(f"{painting} - [Ver imagen]({link})")
