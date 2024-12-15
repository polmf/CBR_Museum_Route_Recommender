import streamlit as st
import json
from helpers.mapa_museu import mark_room_by_number, generate_museum_layout
import matplotlib.pyplot as plt

def render(routa):
    """Función para renderizar días, salas y cuadros usando Streamlit."""
    # Obtener lista de días únicos
    with open('data/base_de_dades_final.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    rutes_recomanades_total = [
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
        for item in data if 'ruta_quadres' in item
    ]

    # Aquí agafem només la primera ruta de la llista, en comptes de les tres primeres
    rutes_recomanades_finals = rutes_recomanades_total[:1]  # Aconsegueix només una ruta

    # Es crea un conjunt de dies per escollir
    all_days = {entry["day"] for ruta in rutes_recomanades_finals for entry in ruta["ruta_quadres"]}
    selected_day = st.selectbox("Selecciona el día", sorted(all_days))

    # Filtrar per dia seleccionat
    filtered_rutas = [
        entry
        for ruta in rutes_recomanades_finals
        for entry in ruta["ruta_quadres"]
        if entry["day"] == selected_day
    ]

    # Obtener lista de salas únicas para el día seleccionado
    all_rooms = {room["room"] for entry in filtered_rutas for room in entry["rooms"]}
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
        for room in entry["rooms"]:
            if room["room"] == selected_room:
                # Extraemos solo los nombres de los cuadros de las sublistas
                paintings = [painting[0] for painting in room['paintings']]
                links = [painting[1] for painting in room['paintings']]  # Obtenemos los enlaces de las imágenes

                # Mostrar los cuadros uno debajo del otro con enlaces para ver la imagen
                for painting, link in zip(paintings, links):
                    st.write(f"{painting} - [Ver imagen]({link})")
