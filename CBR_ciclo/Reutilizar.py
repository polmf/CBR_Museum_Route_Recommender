import pandas as pd

class Reutilizar:
    """
    Clase que se encarga de reutilizar casos previos para recomendar una visita.

    Una vez que tenemos el caso más similar, debemos adaptarlo a las necesidades del 
    nuevo usuario. Esto podría incluir ajustes en la duración de la ruta, la dificultad, etc. 
    Si un usuario prefiere rutas de menos de 2 horas y la ruta recomendada dura 3 horas, 
    la ruta debe ser ajustada.

    Se deberia de recomendar hasta 3 rutas diferentes para que el usuario pueda elegir la que más le guste.
    """

    def __init__(self, user_to_recommend, top_5_similar_users):
        self._base_de_casos = pd.read_csv("data/base_de_dades.csv")
        self.user_to_recommend = user_to_recommend
        self.top_5_similar_users = top_5_similar_users

    def get_route_more_repeated_from_similar_cases(self):
        """
        Obtiene la ruta más repetida entre los casos similares.
        """
        routes = []
        for user_id, _ in self.top_5_similar_users:
            user_data = self._base_de_casos[self._base_de_casos['visitante_id'] == user_id]
            user_routes = user_data['ruta'].tolist()
            routes.extend(user_routes)
            print(routes)
        # Calcular la ruta más repetida
        route_counts = {}
        for route in routes:
            if route.get_nom() in route_counts:
                route_counts[route.get_nom()] += 1
            else:
                route_counts[route.get_nom()] = 1

        most_common_route = max(route_counts, key=route_counts.get)
        return most_common_route
    
    def adjust_route_to_user_preferences(self, route):
        """
        Ajusta la ruta recomendada a las preferencias del nuevo usuario.
        """
        # Ajustar la duración de la ruta
        """if route.get_temps() > self.user_to_recommend.get_hores():
            route.get_temps() = self.user_to_recommend.get_hores()"""
        
        # Ajustar la dificultad de la ruta
        """if route.difficulty > self.user_to_recommend.max_difficulty:
            route.difficulty = self.user_to_recommend.max_difficulty"""
        
        # Otros ajustes basados en las preferencias del usuario
        # ...
        
        return route
