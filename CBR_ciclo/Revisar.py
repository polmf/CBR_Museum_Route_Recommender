
class Revisar:
    """
    Clase que representa la acción de revisar un caso.
    Recoger el feedback del usuario y, si no está satisfecho, realizar ajustes en las rutas futuras.
    """

    def __init__(self, ruta):
        self.feedback = None
        self.ruta = ruta

    def collect_feedback(self):
        """
        Recoge el feedback del usuario sobre la ruta recomendada.
        """
        print("¿Estás satisfecho con la ruta recomendada?")
        feedback = input("Introduce una puntuación del 1 al 5 a la ruta final recomendada (siendo 1 muy insatisfecho y 5 muy satisfecho): ")
        
        return feedback
    
    def print_routes(self):
        """
        Muestra las rutas recomendadas al usuario.
        """
        print("Estas son las rutas recomendadas para ti:")
        # Mostrar rutas
        return self.ruta