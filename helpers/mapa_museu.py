import matplotlib.pyplot as plt
import matplotlib.patches as patches
import imageio
import os
import json

# Layout del museu: generem 108 sales organitzades en una graella
def generate_museum_layout(rows=12, cols=9):
    layout = []
    for i in range(rows):
        for j in range(cols):
            sala_name = f"Sala {i * cols + j + 1}"
            layout.append({"name": sala_name, "coords": (j * 3 + 1, i * 3 + 1), "size": (2, 2)})
    return layout

# Crear el museu base amb sales i passadissos
def draw_museum(ax, MUSEU_LAYOUT, highlight_room=None):
    """
    Dibuixa el museu amb sales i passadissos, destacant la sala especificada si es proporciona.
    """
    for sala in MUSEU_LAYOUT:
        x, y = sala["coords"]
        w, h = sala["size"]
        
        if sala["name"] == highlight_room:
            # Resaltar la sala con un borde rojo si se selecciona
            rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor="red", facecolor="yellow")
        else:
            rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor="black", facecolor="lightgray")
        
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, sala["name"], ha="center", va="center", fontsize=5)

    # Configurar els límits
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 40)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Mapa del Museu", fontsize=14)

# Coordenades de cada sala
def get_room_coords(room_name, MUSEU_LAYOUT):
    """
    Retorna les coordenades del centre d'una sala donat el seu nom.
    """
    for sala in MUSEU_LAYOUT:
        if sala["name"] == room_name:
            x, y = sala["coords"]
            w, h = sala["size"]
            return x + w / 2, y + h / 2
    return None

def mark_room_by_number(room_number, MUSEU_LAYOUT):
    """
    Marca una sala específica en el museu donant el número de sala i retorna el plot.
    """
    room_name = f"Sala {room_number}"
    fig, ax = plt.subplots(figsize=(15, 20))
    draw_museum(ax, MUSEU_LAYOUT, highlight_room=room_name)
    return fig 

# Crear un gif per cada dia
def create_day_gif(day, route, idx, MUSEU_LAYOUT, output_dir="museum_videos"):
    # Crear el directorio si no existe
    os.makedirs(output_dir, exist_ok=True)
    frames = []

    # Crear la figura del museo
    fig, ax = plt.subplots(figsize=(15, 20))  # Ajustem la mida del museu
    draw_museum(ax, MUSEU_LAYOUT)

    # Simular el moviment per les sales
    prev_coords = None
    for room in route:
        x, y = get_room_coords(room, MUSEU_LAYOUT)
        if x is not None and y is not None:
            # Simular moviment per passadissos
            if prev_coords:
                move_through_corridors(ax, prev_coords, (x, y))
            
            # Afegir marcador (persona) a la sala actual
            ax.add_patch(plt.Circle((x, y), 0.3, color="red"))
            ax.text(x, y, "👤", ha="center", va="center", fontsize=12)

            # Marcar la sala com a visitada
            sala_rect = patches.Rectangle((x - 1, y - 1), 2, 2, linewidth=2, edgecolor="blue", facecolor="lightblue")
            ax.add_patch(sala_rect)

            # Guardar el frame
            frame_path = os.path.join(output_dir, f"route_{idx}_day_{day}_frame_{room}.png")  # Incluimos el índice en el nombre
            plt.savefig(frame_path)
            frames.append(frame_path)

            # Eliminar el marcador para el siguiente frame
            prev_coords = (x, y)
            ax.patches[-1].remove()
    
    # Crear el gif con el índice de la ruta en el nombre
    gif_path = os.path.join(output_dir, f"museum_route_{idx}_day_{day}.mp4")  # Incluimos el índice en el nombre del gif
    images = [imageio.imread(frame) for frame in frames]
    imageio.mimsave(gif_path, images, fps=1)
    plt.close(fig)

    print(f"Gif de la ruta {idx} para el día {day} creado en {gif_path}")

# Simular moviment pels passadissos
def move_through_corridors(ax, start, end):
    """
    Simula el moviment d'una persona pels passadissos.
    """
    x1, y1 = start
    x2, y2 = end
    path_x = [x1, x1, x2]
    path_y = [y1, y2, y2]
    ax.plot(path_x, path_y, color="orange", linestyle="--", linewidth=1)

# Ruta d'exemple
"""ruta_recomanada = {
    "ruta_quadres": [
        {"day": 1, "rooms": ["Sala 1", "Sala 2", "Sala 12", "Sala 15"]},
        {"day": 2, "rooms": ["Sala 20", "Sala 34", "Sala 45", "Sala 60"]},
    ]
}"""

def fer_rutes(rutes_per_recomanar):
    MUSEU_LAYOUT = generate_museum_layout()
    

    # Crear una lista con las rutas completas de 'ruta_quadres'
    """rutes_recomanades_total = [
        {
            "ruta_quadres": [
                {"day": entry["day"], "rooms": list(entry["rooms"].keys())}
                for entry in item['ruta_quadres']
            ]
        }
        for item in data if 'ruta_quadres' in item
    ]"""
    

    rutes_recomanades_total = [
        {
            "ruta_quadres": [
                {"day": ruta['ruta_quadres'][0]["day"], "rooms": list(ruta['ruta_quadres'][0]["rooms"].keys())}
                for ruta in rutes_per_recomanar
            ]
        }
    ]
    

    # Crear gifs por cada día y acceder al índice
    for idx, ruta_recomanada in enumerate(rutes_recomanades_total):
        for dia in ruta_recomanada["ruta_quadres"]:
            print(dia)
            create_day_gif(dia["day"], dia["rooms"], idx + 1, MUSEU_LAYOUT)

#fer_rutes()