import matplotlib.pyplot as plt
import matplotlib.patches as patches
import imageio
import os

# Layout del museu: generem 108 sales organitzades en una graella
def generate_museum_layout(rows=12, cols=9):
    layout = []
    for i in range(rows):
        for j in range(cols):
            sala_name = f"Sala {i * cols + j + 1}"
            layout.append({"name": sala_name, "coords": (j * 3 + 1, i * 3 + 1), "size": (2, 2)})
    return layout

MUSEU_LAYOUT = generate_museum_layout()

# Crear el museu base amb sales i passadissos
def draw_museum(ax):
    """
    Dibuixa el museu amb sales i passadissos.
    """
    for sala in MUSEU_LAYOUT:
        x, y = sala["coords"]
        w, h = sala["size"]
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
def get_room_coords(room_name):
    """
    Retorna les coordenades del centre d'una sala donat el seu nom.
    """
    for sala in MUSEU_LAYOUT:
        if sala["name"] == room_name:
            x, y = sala["coords"]
            w, h = sala["size"]
            return x + w / 2, y + h / 2
    return None

# Crear un gif per cada dia
def create_day_gif(day, route, output_dir="museum_gifs"):
    os.makedirs(output_dir, exist_ok=True)
    frames = []
    
    fig, ax = plt.subplots(figsize=(15, 20))  # Ajustem la mida del museu
    draw_museum(ax)

    # Simular el moviment per les sales
    prev_coords = None
    for room in route:
        x, y = get_room_coords(room)
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
            frame_path = os.path.join(output_dir, f"day_{day}_frame_{room}.png")
            plt.savefig(frame_path)
            frames.append(frame_path)

            # Eliminar el marcador per al següent frame
            prev_coords = (x, y)
            ax.patches[-1].remove()
    
    # Crear el gif
    gif_path = os.path.join(output_dir, f"museum_route_day_{day}.gif")
    images = [imageio.imread(frame) for frame in frames]
    imageio.mimsave(gif_path, images, fps=1)
    plt.close(fig)
    print(f"Gif del dia {day} creat a {gif_path}")

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
ruta_recomanada = {
    "ruta_quadres": [
        {"day": 1, "rooms": ["Sala 1", "Sala 2", "Sala 12", "Sala 15"]},
        {"day": 2, "rooms": ["Sala 20", "Sala 34", "Sala 45", "Sala 60"]},
    ]
}

# Crear gifs per cada dia
for dia in ruta_recomanada["ruta_quadres"]:
    create_day_gif(dia["day"], dia["rooms"])