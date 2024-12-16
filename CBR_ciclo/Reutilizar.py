from typing import Dict, List, Tuple, Union
import pandas as pd
from generacio.classes import Visitant, Quadre
import json
from datetime import datetime
from generacio.recom_clips import calculate_observation_time


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
        self._base_de_casos = pd.read_json("data/base_de_dades_final.json")
        with open('data/quadres.json', 'r', encoding='utf-8') as f_quadres:
            quadres_data = json.load(f_quadres)
            quadres = [Quadre.from_dict(data) for data in quadres_data]
        
        self.quadres = quadres
        self.top_3_similar_cases = top_3_similar_cases
        self.user_to_recommend = user_to_recommend

    def get_instancies(self, quadres_ruta):
        instancies = []
        for quadre_ruta in quadres_ruta:
            found = next((quadre for quadre in self.quadres if quadre_ruta == quadre.nom), None)
            instancies.append(found if found else quadre_ruta)
        return instancies


    def get_route_from_similar_cases(
        self,
        top_3_similar_cases: List[Tuple[int, float]]
    ):
        routes = {}
        for index, _ in top_3_similar_cases:
            user_data = self._base_de_casos.iloc[index]
            user_routes = user_data['ruta']
            
            ruta_info = {
                'ruta': user_data['ruta'],
                'quadres': user_data['ruta_quadres_list'],
                'temps': user_data['ruta_temps'],
                'puntuacio': user_data['puntuacio_ruta']
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
            cuadro for cuadro in self.quadres 
            if cuadro.autor in artistas and cuadro.nom not in route['quadres']
        ]
        route['quadres'].extend(cuadros_a_añadir)
        return route

    def adapt_route_to_user_preferences(self, route: Dict[str, Union[str, int]]):
        """
        Adapta la ruta a las preferencias del usuario.
        """
        temps_user_to_recommend = self.user_to_recommend.hores * self.user_to_recommend.dies * 60
        temps_ruta = route['temps']
        
        if temps_ruta > temps_user_to_recommend:  # Si la ruta dura más de lo que el usuario quiere
            cuadros_ordenados = sorted(
                route['quadres'], 
                key=lambda x: next((q.rellevancia for q in self.quadres if q.nom == x), 0)
            )
            while temps_ruta > temps_user_to_recommend and cuadros_ordenados:
                cuadro_a_remover = cuadros_ordenados.pop(0)
                route['quadres'].remove(cuadro_a_remover)

                temps_ruta -= calculate_observation_time(
                    next(q for q in self.quadres if q.nom == cuadro_a_remover),
                    (1 + 0.04 * (self.user_to_recommend.coneixements - 1))
                )

        else:  # Si la ruta dura menos de lo que el usuario quiere
            while temps_ruta < temps_user_to_recommend:
                if isinstance(self.user_to_recommend.interessos_autor, list):
                    route = self.add_artist(self.user_to_recommend.interessos_autor, route)

                cuadros_relevantes = sorted(
                    self.quadres, 
                    key=lambda x: x.rellevancia, 
                    reverse=True
                )
                for cuadro in cuadros_relevantes:
                    if cuadro.nom not in route['quadres']:
                        route['quadres'].append(cuadro.nom)
                        temps_ruta += calculate_observation_time(cuadro, 1 + 0.04 * (self.user_to_recommend.coneixements - 1))
                        if temps_ruta >= temps_user_to_recommend:
                            break

        # Actualizamos el tiempo y obtenemos las instancias de los cuadros
        route['temps'] = temps_ruta
        route['instancies'] = self.get_instancies(route['quadres'])

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

