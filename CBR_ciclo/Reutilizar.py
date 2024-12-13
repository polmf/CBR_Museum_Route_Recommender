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
        self._base_de_casos = pd.read_csv("data/base_de_dades.csv")
        # TODO
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
            
            if user_routes in routes:
                routes[user_routes].append(ruta_info)
            else:
                routes[user_routes] = [ruta_info]

        return routes
    
    def add_artist(artistas, route):
        if artistas :
            pass
    
    def adapt_route_to_user_preferences(
        self,
        route: Dict[str, Union[str, int]]
        ):

        # Ajustar la duración de la ruta
        temps_user_to_recommend = self.user_to_recommend.hores * self.user_to_recommend.dies * 60
        temps_ruta = route['temps']
        
        if temps_ruta > temps_user_to_recommend: # Si la ruta dura más de lo que el usuario quiere
            # traiem quadres menys rellevants de la ruta fins que la duració sigui menor

            pass

        else: # Si la ruta dura menos de lo que el usuario quiere
                # afegim quadres rellevants de la ruta fins que la duració sigui major
            print("Ruta:", route)
            print()
            print("----"*30)
            print()
            """
            Ajusta la ruta recomendada a las preferencias del nuevo usuario.
            """
            # Ajustar los artistas y estilos de la ruta 
            # Si en la base de datos hay cuadros de artistas que le gustan al usuario, añadirlos a la ruta
            artistas = self.user_to_recommend.interessos_autor
            print("Artistas:", artistas)
            quadres_artistas = [quadre for quadre in self.quadres if quadre.autor in artistas]

            for quadre in quadres_artistas:
                
                if quadre not in route['quadres']:
                    route['quadres'].append(quadre)

            # Si en la base de datos hay cuadros de estilos que le gustan al usuario, añadirlos a la ruta
            pass

        if route['puntuacio'] < 3:
            # SI la puntuació de la ruta és baixa -> fer algo
            pass
        
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
