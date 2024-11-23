import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean

class Recuperar:
    """
    Clase que se encarga de recuperar casos previos para recomendar una visita.
    """
    
    def __init__(self, user_to_recommend):
        self._base_de_casos = pd.read_csv("data/base_de_casos.csv")
        self.user = user_to_recommend

    def calculate_user_similarity(self, user1, user2):
        """
        Calcula la similitud entre dos usuarios usando la distancia euclidiana.
        """
        # Definir las características relevantes para la similitud
        user1_profile = [user1['edad'], user1['estudis'], user1['coneixement'], user1['interessos_autor'], user1['interessos_estils']]
        user2_profile = [user2['edad'], user2['estudis'], user2['coneixement'], user2['interessos_autor'], user2['interessos_estils']]
        
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
            if other_user['visitante_id'] != user_id:
                similarity = self.calculate_user_similarity(self.user, other_user)
                similarities.append((other_user['visitante_id'], similarity))
        
        # Ordenar los usuarios por similitud y devolver los primeros num_users
        similarities.sort(key=lambda x: x[1])
        similar_users = similarities[:num_users]
        
        return similar_users
    
    def get_routes_of_similar_users(top_5_similar_users, all_users_data):
        """
        Obtiene las rutas de los 5 usuarios más similares.
        """
        routes = []
        
        # Para cada usuario similar, recuperar sus rutas
        for user_id, _ in top_5_similar_users:
            user_data = next(user for user in all_users_data if user['id'] == user_id)
            user_routes = user_data['rutas']  # Suponemos que las rutas están en 'rutas'
            routes.extend(user_routes)
        
        return routes