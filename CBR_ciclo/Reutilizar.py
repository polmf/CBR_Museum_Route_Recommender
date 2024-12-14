from typing import Dict, List, Tuple, Union
import pandas as pd
from generacio.classes import Visitant
from transformations.functions import normalization
from scipy.spatial.distance import cosine, hamming
from generacio.classes import Visitant
from generacio.classes import Quadre
from generacio.classes import Sala
from generacio.classes import Autor
import json

class Reutilizar:
    """
    Clase que se encarga de reutilizar casos previos para recomendar una visita.

    Una vez que tenemos el caso más similar, debemos adaptarlo a las necesidades del 
    nuevo usuario. Esto podría incluir ajustes en la duración de la ruta, la dificultad, etc. 
    Si un usuario prefiere rutas de menos de 2 horas y la ruta recomendada dura 3 horas, 
    la ruta debe ser ajustada.

    Se deberia de recomendar hasta 3 rutas diferentes para que el usuario pueda elegir la que más le guste.
    """

    def __init__(self, user_to_recommend: Visitant, top_3_similar_cases: pd.DataFrame):
        self._base_de_casos = pd.read_csv("datos.csv")
        with open('data/quadres.json', 'r', encoding='utf-8') as f_quadres:
            quadres_data = json.load(f_quadres)
            quadres = [Quadre.from_dict(data) for data in quadres_data]
        
        self.quadres = quadres


        self.top_3_similar_cases = top_3_similar_cases
        self.user_to_recommend = user_to_recommend

    def get_route_from_similar_cases(
        self,
        top_3_similar_cases: List[Tuple[str, float]]
        ):

        routes = {}
        for index, _ in top_3_similar_cases:
            user_data = self._base_de_casos.iloc[index]
            user_routes = user_data['ruta']
            
            ruta_info = {
                'quadres': user_data['ruta_quadres'],
                'temps': user_data['ruta_temps'],
                'puntuacio': user_data['puntuacio_ruta']
            }
            # TODO
            # AÑADIR EN LA COLUMNA DE ULTIMA VISITA LA DATA ACTUAL Y EN LA DE VISITAS LA CANTIDAD DE VISITAS + 1
            if user_routes in routes:
                routes[user_routes].append(ruta_info)
            else:
                routes[user_routes] = [ruta_info]

        return routes
    
    def add_artist(artistas, route):
        # Añaadir cuadros de artistas que le gustan al usuario
        # TODO
    


    def adapt_route_to_user_preferences(
        self,
        route: Dict[str, Union[str, int]]
        ):

        # Ajustar la duración de la ruta
        temps_user_to_recommend = self.user_to_recommend.hores * self.user_to_recommend.dies * 60
        temps_ruta = route['temps']
        
        if temps_ruta > temps_user_to_recommend: # Si la ruta dura más de lo que el usuario quiere
            # Quitamos cuadros poco relevantes de la ruta hasta que la duración sea menor
            # TODO
            pass

        else: # Si la ruta dura menos de lo que el usuario quiere
            
            # Mientras la duración de la ruta sea menor a la que el usuario quiere
                # TODO
            # Añadimos cuadros de artistas que le gustan al usuario

            # Añadimos cuadros relevantes

        # EVALUAMOS LA RUTA CON NUESTRO AGENTE
        # SI LA EVALUACIÓN DE LA RUTA ES BUENA O MALA
        # LA AÑADIMOS A LA BASE DE CASOS
        
        return route
    
    def recommend_routes(self):
        """
        Recomienda hasta 3 rutas diferentes para que el usuario pueda elegir la que más le guste.
        """
        routes = self.get_route_from_similar_cases(self.top_3_similar_cases)
        print("Rutes:", routes)
        routes = [
            self.adapt_route_to_user_preferences(route) 
            for route_list in routes.values() 
            for route in route_list
        ]

        top_3_routes = sorted(routes, key=lambda x: x['NOVA PUNTUACIO'], reverse=True)[:3] # TO DO

        return top_3_routes
