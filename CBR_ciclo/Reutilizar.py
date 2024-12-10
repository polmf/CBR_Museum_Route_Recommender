from typing import Dict, List, Tuple, Union
import pandas as pd
from generacio.classes import Visitant
from transformations.functions import normalization
from scipy.spatial.distance import cosine, hamming

class Reutilizar:
    """
    Clase que se encarga de reutilizar casos previos para recomendar una visita.

    Una vez que tenemos el caso más similar, debemos adaptarlo a las necesidades del 
    nuevo usuario. Esto podría incluir ajustes en la duración de la ruta, la dificultad, etc. 
    Si un usuario prefiere rutas de menos de 2 horas y la ruta recomendada dura 3 horas, 
    la ruta debe ser ajustada.

    Se deberia de recomendar hasta 3 rutas diferentes para que el usuario pueda elegir la que más le guste.
    """

    def __init__(self, user_to_recommend: Visitant, top_10_similar_cases: pd.DataFrame):
        self._base_de_casos = pd.read_csv("data/base_de_dades.csv")
        self.top_10_similar_cases = top_10_similar_cases
        self.user_to_recommend = user_to_recommend

    def get_route_from_similar_cases(
        self,
        top_10_similar_cases: List[Tuple[str, float]]
        ):

        routes = {}
        for index, _ in top_10_similar_cases:
            user_data = self._base_de_casos.iloc[index]
            user_routes = user_data['ruta']
            
            ruta_info = {
                'quadres': user_data['ruta_quadres'],
                'temps': user_data['ruta_temps'],
                'puntuacio': user_data['puntuacio_ruta']
            }
            
            if user_routes in routes:
                routes[user_routes].append(ruta_info)
            else:
                routes[user_routes] = [ruta_info]

        return routes
    
    def adapt_route_to_user_preferences(
        self,
        route: Dict[str, Union[str, int]]
        ):
        """
        Ajusta la ruta recomendada a las preferencias del nuevo usuario.
        """
        # Ajustar la duración de la ruta
        temps_user_to_recommend = self.user_to_recommend.hores * self.user_to_recommend.dies * 60
        temps_ruta = route['temps']
        
        if temps_ruta > temps_user_to_recommend:
            # traiem quadres menys rellevants de la ruta fins que la duració sigui menor
            pass
        else:
            # afegim quadres rellevants de la ruta fins que la duració sigui major
            pass

        if route['puntuacio'] < 3:
            pass
        
        return route
    
    def recommend_routes(self):
        """
        Recomienda hasta 3 rutas diferentes para que el usuario pueda elegir la que más le guste.
        """
        routes = self.get_route_from_similar_cases(self.top_10_similar_cases)
        routes = [
            self.adapt_route_to_user_preferences(route) 
            for route_list in routes.values() 
            for route in route_list
        ]

        top_3_routes = sorted(routes, key=lambda x: x['puntuacio'], reverse=True)[:3]

        return top_3_routes
