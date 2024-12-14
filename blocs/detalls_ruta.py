import streamlit as st
import json

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

    # Filtrar y mostrar cuadros
    for entry in filtered_rutas:
        for room in entry["rooms"]:
            if room["room"] == selected_room:
                # Extraemos solo los nombres de los cuadros de las sublistas
                paintings = [painting[0] for painting in room['paintings']]
                # Mostrar los cuadros uno debajo del otro
                for painting in paintings:
                    st.write(painting)
