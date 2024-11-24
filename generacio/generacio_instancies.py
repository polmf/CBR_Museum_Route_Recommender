import re
from classes import Quadre, Sala, Autor

def assign_salas(cuadros):
    # Mapeo de estilos a números de sala
    estilo_a_sala = {}
    sala_num = 1
    salas = {}  # Usamos un diccionario para almacenar las salas

    for cuadro in cuadros:
        if cuadro.estil not in estilo_a_sala:
            estilo_a_sala[cuadro.estil] = sala_num
            salas[sala_num] = Sala(sala=sala_num)  # Crear la sala en el diccionario
            sala_num += 1
        cuadro.sala = estilo_a_sala[cuadro.estil]

    return salas

def parse_cuadros(file_path):
    cuadros = []
    autores = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().strip()
        # Dividir el archivo por bloques de texto de cada cuadro
        obras = content.split("\n\n")  # Suponemos que hay una línea en blanco entre cada cuadro

        for obra in obras:
            # Dividir la obra en líneas individuales
            lines = obra.splitlines()

            # Crear un diccionario para almacenar los valores de las propiedades
            datos = {}

            # Extraer las propiedades de cada línea
            for line in lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    datos[key.strip()] = value.strip()

            # Asignar valores por clave
            nom = datos.get("Nom", "Nombre desconocido")
            any = datos.get("Any", "Año desconocido")
            epoca = datos.get("Època", "Época desconocida")
            estil = datos.get("Estil", "Estilo desconocido")
            autor = datos.get("Autor", "Autor desconocido")
            sala = datos.get("Sala", "Sala desconocida")
            tema = datos.get("Tema", "Tema desconocido")
            dimensions = datos.get("Dimensions", "Dimensiones desconocidas")
            complexitat = int(datos.get("Complexitat", 3))
            rellevancia = int(datos.get("Rellevància", 3))
            tecnica = datos.get("Tècnica", "Técnica desconocida")
            suport = datos.get("Suport", "Soporte desconocido")
            conservacio = int(datos.get("Estat de conservació", 3))

            # Procesar las dimensiones (extraer altura y anchura)
            try:
                # Buscar las dimensiones en formato "alto x ancho cm"
                dimensions_match = re.search(r"(\d+)[\s]*x[\s]*(\d+)", dimensions)
                if dimensions_match:
                    alçada = int(dimensions_match.group(1))
                    amplada = int(dimensions_match.group(2))
                else:
                    alçada, amplada = 30, 30  # Valores predeterminados si no se encuentran las dimensiones
            except ValueError:
                alçada, amplada = 30, 30  # Valores predeterminados si no se pueden convertir

            # Crear una nueva instancia de la clase Quadre
            cuadro = Quadre(
                nom=nom,
                alçada=alçada,
                amplada=amplada,
                any=any,
                autor=autor,
                sala=sala,
                complexitat=complexitat,
                conservacio=conservacio,
                tema=tema,
                epoca=epoca,
                estil=estil,
                rellevancia=rellevancia
            )

            # Agregar el cuadro a la lista
            cuadros.append(cuadro)

            # Registrar el autor si no está ya en el diccionario de autores
            if autor not in autores:
                autores[autor] = Autor(nom=autor, epoca=epoca, estils=[estil])
            else:
                # Si ya existe, añadir el estilo a la lista de estilos
                if estil not in autores[autor].estils:
                    autores[autor].estils.append(estil)

    # Devolver la lista de cuadros y autores
    return cuadros, autores

# Ejecutar el script
if __name__ == "__main__":
    file_path = "data/cuadros.txt"  # Cambia la ruta al archivo real
    cuadros, autores = parse_cuadros(file_path)

    # Asignar las salas según el estilo de cada cuadro
    salas = assign_salas(cuadros)

    # Mostrar las instancias de los cuadros creados con la sala asignada
    for cuadro in cuadros:
        print(f"Cuadro: {cuadro.nom}, Año: {cuadro.any}, Autor: {cuadro.autor}, Tema: {cuadro.tema}, Sala: {cuadro.sala}")

    # Mostrar autores y sus estilos
    print("\nAutores:")
    for autor in autores.values():
        print(f"{autor.nom}, Época: {autor.epoca}, Estilos: {', '.join(autor.estils)}")

    # Mostrar salas con su número
    print("\nSalas:")
    for sala in salas.values():
        print(f"Sala: {sala.sala}")
