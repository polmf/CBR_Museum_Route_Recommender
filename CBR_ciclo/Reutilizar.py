from typing import Dict, List, Tuple, Union
import pandas as pd
from generacio.classes import Visitant, Quadre, Sala, Autor
from transformations.functions import normalization
from scipy.spatial.distance import cosine, hamming
import json
from datetime import datetime


class Reutilizar:
    """
    Clase que se encarga de reutilizar casos previos para recomendar una visita.

    Una vez que tenemos el caso más similar, debemos adaptarlo a las necesidades del 
    nuevo usuario. Esto podría incluir ajustes en la duración de la ruta, la dificultad, etc. 
    Si un usuario prefiere rutas de menos de 2 horas y la ruta recomendada dura 3 horas, 
    la ruta debe ser ajustada.

    Se debería recomendar hasta 3 rutas diferentes para que el usuario pueda elegir la que más le guste.
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
        top_3_similar_cases: List[Tuple[int, float]]
    ):
        routes = {}
        for index, _ in top_3_similar_cases:
            user_data = self._base_de_casos.iloc[index]
            user_routes = user_data['ruta']
            
            ruta_info = {
                'quadres': user_data['cuadros_visitados'].split(", "),
                'temps': user_data['ruta_temps'],
                'puntuacio': user_data['puntacio_ruta']
            }

            # Añadir información de última visita y actualizar las visitas
            self._base_de_casos.loc[index, 'ultima_visita'] = datetime.now().strftime("%Y-%m-%d")
            self._base_de_casos.loc[index, 'recompte_utilitzat'] += 1

            if user_routes in routes:
                routes[user_routes].append(ruta_info)
            else:
                routes[user_routes] = [ruta_info]

        return routes
    
    def add_artist(self, artistas: List[str], route: Dict):
        """
        Añadir cuadros de artistas que le gustan al usuario.
        """
        cuadros_a_añadir = [
            cuadro.nom for cuadro in self.quadres 
            if cuadro.autor.nom in artistas and cuadro.nom not in route['quadres']
        ]
        route['quadres'].extend(cuadros_a_añadir)
        return route

    def adapt_route_to_user_preferences(
        self,
        route: Dict[str, Union[str, int]]
    ):
        """
        Adapta la ruta a las preferencias del usuario.
        """
        temps_user_to_recommend = self.user_to_recommend.hores * self.user_to_recommend.dies * 60
        temps_ruta = route['temps']
        
        if temps_ruta > temps_user_to_recommend:  # Si la ruta dura más de lo que el usuario quiere
            # Quitamos cuadros poco relevantes de la ruta hasta que la duración sea menor
            cuadros_ordenados = sorted(
                route['quadres'], 
                key=lambda x: next((q.rellevancia for q in self.quadres if q.nom == x), 0)
            )
            while temps_ruta > temps_user_to_recommend and cuadros_ordenados:
                cuadro_a_remover = cuadros_ordenados.pop(0)
                route['quadres'].remove(cuadro_a_remover)
                temps_ruta -= calculate_observation_time(
                    next(q for q in self.quadres if q.nom == cuadro_a_remover),
                    self.user_to_recommend.coneixement
                )

        else:  # Si la ruta dura menos de lo que el usuario quiere
            while temps_ruta < temps_user_to_recommend:
                # Añadimos cuadros de artistas que le gustan al usuario
                route = self.add_artist(self.user_to_recommend.interessos_autor, route)

                # Añadimos cuadros relevantes
                cuadros_relevantes = sorted(
                    self.quadres, 
                    key=lambda x: x.rellevancia, 
                    reverse=True
                )
                for cuadro in cuadros_relevantes:
                    if cuadro.nom not in route['quadres']:
                        route['quadres'].append(cuadro.nom)
                        temps_ruta += calculate_observation_time(cuadro, self.user_to_recommend.coneixement)
                        if temps_ruta >= temps_user_to_recommend:
                            break


        # Actualizar la base de casos
        self._base_de_casos = self._base_de_casos.append({
            'ruta': "Nueva ruta adaptada",
            'ruta_temps': temps_ruta,
            'puntacio_ruta': route['puntuacio'],
            'cuadros_visitados': ", ".join(route['quadres']),
            'ultima_visita': datetime.now().strftime("%Y-%m-%d"),
            'visitant_visites': 1
        }, ignore_index=True)
        
        return route
    
    def recommend_routes(self):
        """
        Recomienda hasta 3 rutas diferentes para que el usuario pueda elegir la que más le guste.
        """
        routes = self.get_route_from_similar_cases(self.top_3_similar_cases)
        routes = [
            self.adapt_route_to_user_preferences(route) 
            for route_list in routes.values() 
            for route in route_list
        ]

        return routes


def calculate_observation_time(painting, knowledge_factor):
    """
    Calcula el tiempo de observación de un cuadro en función de su complejidad,
    relevancia, tamaño y el factor de conocimiento del usuario.
    """
    complexity = painting.complexitat
    dim_cm2 = painting.dim_cm2
    relevance = painting.rellevancia

    base_time = 1.0 if dim_cm2 < 5007 else 2.0

    complexity_factor = (
        1.1 if complexity <= 2 else
        1.2 if complexity <= 4 else
        1.3 if complexity <= 6 else
        1.4 if complexity <= 8 else
        1.5
    )

    relevance_factor = (
        1.1 if relevance <= 2 else
        1.2 if relevance <= 4 else
        1.3 if relevance <= 6 else
        1.4 if relevance <= 8 else
        1.5
    )
    
    total_time = base_time * complexity_factor * relevance_factor * knowledge_factor
    return round(total_time)