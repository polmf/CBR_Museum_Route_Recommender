import json
import csv

# Cargar el archivo JSON
with open("data/base_dades_normalitzades.json", "r") as json_file:
    data = json.load(json_file)

# Crear una lista para almacenar las filas del CSV
csv_data = []

# Coger un subconjunto de datos para probar

# Procesar cada visitante
for visitante in data:
    base_row = {
        "visitante_id": visitante["visitante_id"],
        "visitant_edat": visitante["visitant_edat"],
        "visitant_visites": visitante["visitant_visites"],
        "visitant_dies": visitante["visitant_dies"],
        "visitant_hores": visitante["visitant_hores"],
        "visitant_companyia": visitante["visitant_companyia"],
        "visitant_estudis": visitante["visitant_estudis"],
        "visitant_coneixement": visitante["visitant_coneixement"],
        "visitant_quizz": visitante["visitant_quizz"],
        "ruta": visitante["ruta"],
        "ruta_temps": visitante["ruta_temps"],
        "puntuacio_ruta": visitante["puntuacio_ruta"],
    }

    # Unir intereses de autor, estilos y tipos como strings separados por comas
    base_row["visitant_interessos_autor"] = ", ".join(visitante["visitant_interessos_autor"])
    base_row["visitant_interessos_estils"] = ", ".join(visitante["visitant_interessos_estils"])
    base_row["visitant_interessos_tipus"] = ", ".join(visitante["visitant_interessos_tipus"])
    
    # Consolidar salas y cuadros visitados
    salas_visitadas = set()  # Para evitar duplicados
    cuadros_visitados = []  # Lista para cuadros

    for dia in visitante["ruta_quadres"]:
        for room, cuadros in dia["rooms"].items():
            salas_visitadas.add(room)  # Agregar sala al conjunto
            for cuadro in cuadros:
                cuadros_visitados.append(cuadro[0])  # Agregar nombre del cuadro a la lista

    # Añadir las nuevas columnas al registro base
    base_row["salas_visitadas"] = ", ".join(sorted(salas_visitadas))  # Convertir a string ordenado
    base_row["cuadros_visitados"] = ", ".join(cuadros_visitados)  # Lista de cuadros

    # Añadir la fila consolidada al CSV
    csv_data.append(base_row)

# Guardar el archivo CSV
csv_columns = [
    "visitante_id", "visitant_edat", "visitant_visites", "visitant_dies", "visitant_hores",
    "visitant_companyia", "visitant_estudis", "visitant_coneixement", "visitant_quizz",
    "visitant_interessos_autor", "visitant_interessos_estils", "visitant_interessos_tipus",
    "ruta", "ruta_temps", "puntuacio_ruta", "salas_visitadas", "cuadros_visitados"
]

with open("datos.csv", "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    writer.writeheader()
    writer.writerows(csv_data)

print("Archivo CSV generado como 'datos.csv'")