import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean

class Recuperar:
    """
    Clase que se encarga de recuperar casos previos para recomendar una visita.
    """
    
    def __init__(self, user_to_recommend):
        self._base_de_casos = pd.read_csv("data/base_de_dades.csv")
        self.user = user_to_recommend

    def calculate_user_similarity(self, user1, user2):
        """
        Calcula la similitud entre dos usuarios usando la distancia euclidiana.
        """
        # Definir las características relevantes para la similitud
        user1_profile = [user1.get_edat()] #, user1.get_estudis(), user1.get_coneixements(), user1.get_interessos_autor(), user1.get_interessos_estils()]
        user2_profile = [user2['visitant_edat']] #, user2['visitant_estudis'], user2['visitant_coneixement'], user2['visitant_interessos_autor'], user2['visitant_interessos_estils']]
        
        # Normalización si es necesario (para que todas las características tengan el mismo peso)
        
        # Calcular la distancia euclidiana entre los dos usuarios
        similarity = euclidean(user1_profile, user2_profile)
        
        return similarity
    
    def recommend_similar_users(self, user_id, num_users=5):
        """
        Recomienda usuarios similares al usuario dado.
        """

        # Calcular la similitud con todos los usuarios
        similarities = []
        for _, other_user in self._base_de_casos.iterrows():
            #if other_user['visitante_id'] != user_id:
                similarity = self.calculate_user_similarity(self.user, other_user)
                similarities.append((other_user['visitante_id'], similarity))
        
        # Ordenar los usuarios por similitud y devolver los primeros num_users
        similarities.sort(key=lambda x: x[1])
        similar_users = similarities[:num_users]
        
        return similar_users
    
    def get_routes_of_similar_users(self, top_5_similar_users):
        """
        Obtiene las rutas de los 5 usuarios más similares.
        """
        routes = []
        
        # Para cada usuario similar, recuperar sus rutas
        for user_id, _ in top_5_similar_users:
            user_data = next(user for _, user in self._base_de_casos.iterrows() if user['visitante_id'] == user_id)
            user_routes = user_data['ruta']  # Suponemos que las rutas están en 'rutas'
            routes.extend(user_routes)
        
        return routes