import pandas as pd

class Reutilizar:
    """
    Clase que se encarga de reutilizar casos previos para recomendar una visita.

    Una vez que tenemos el caso más similar, debemos adaptarlo a las necesidades del 
    nuevo usuario. Esto podría incluir ajustes en la duración de la ruta, la dificultad, etc. 
    Si un usuario prefiere rutas de menos de 2 horas y la ruta recomendada dura 3 horas, 
    la ruta debe ser ajustada.
    """

    def __init__(self, user_to_recommend):
        self._base_de_casos = pd.read_csv("data/base_de_casos.csv")
        self.user_to_recommend = user_to_recommend
