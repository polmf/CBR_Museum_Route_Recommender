import pandas as pd
import numpy as np
from transformations.functions import normalization
from scipy.spatial.distance import cosine, hamming

class Recuperar:
    """
    Clase que se encarga de recuperar casos previos para recomendar una visita.
    """
    
    def __init__(self, user_to_recommend):
        self._base_de_casos = pd.read_csv("data/base_de_dades.csv")
        self._base_de_casos_normalized = pd.read_csv("data/base_de_dades_normalized.csv")
        self.user_to_recommend_normalized = normalization(user_to_recommend, self._base_de_casos)
        self.num_cols = [
            'visitant_edat',
            'visitant_visites',
            'visitant_dies',
            'visitant_hores',
            'visitant_coneixement',
            'visitant_quizz',
        ]

        self.cols_to_compare = self.get_cols_to_compare()

        self.cat_cols = self.remove_num_cols()

    def remove_num_cols(self):
        cat_cols = self.cols_to_compare.copy()
        for col in self.num_cols:
            cat_cols.remove(col)

        return cat_cols
    
    def get_cols_to_compare(self):
        cols_to_compare = self._base_de_casos_normalized.columns.to_list()

        return cols_to_compare

    def get_most_similar_cluster(self) -> int:
        self.cols_to_compare.remove('cluster')
        self.cat_cols.remove('cluster')
        
        clusters_representation = {}
        for cluster, data in self._base_de_casos_normalized.groupby('cluster'):
            clusters_representation[cluster] = {}
            for col in self.cols_to_compare:
                clusters_representation[cluster][col] = data[col].mean()
                if col in self.cat_cols:
                    # mes de 0.1 es 1, sino 0
                    clusters_representation[cluster][col] = 1 if clusters_representation[cluster][col] > 0.1 else 0

        clusters_representation_df = pd.DataFrame(clusters_representation, index=self.cols_to_compare).T

        dist_cosine = self.calculate_cosine_similarity(
            self.user_to_recommend_normalized[self.num_cols].iloc[0], 
            clusters_representation_df[self.num_cols]
        )

        dist_hamming = self.calculate_hamming_distance(
            self.user_to_recommend_normalized[self.cat_cols].iloc[0], 
            clusters_representation_df[self.cat_cols]
        )

        dist_total = self.calculate_combined_similarity(
            dist_cosine, 
            dist_hamming
        )

        most_similar_cluster = sorted(dist_total, key=lambda x: x[1])[0][0]

        return most_similar_cluster        
        

    def get_10_most_similar_cases(
        self,
        most_similar_cluster: int
        ) -> pd.DataFrame:
        """
        Obtiene los 10 casos más similares al nuevo usuario.
        """
        similar_cases = self._base_de_casos_normalized[self._base_de_casos_normalized['cluster'] == most_similar_cluster]
        
        # calcular la distancia entre user_to_recommend y los casos similares
        dist_coseno = self.calculate_cosine_similarity(
            self.user_to_recommend_normalized[self.num_cols].iloc[0], 
            similar_cases[self.num_cols]
        )

        dist_hamming = self.calculate_hamming_distance(
            self.user_to_recommend_normalized[self.cat_cols].iloc[0], 
            similar_cases[self.cat_cols]
        )

        dist_total = self.calculate_combined_similarity(
            dist_coseno, 
            dist_hamming
        )
        casos_similares_10 = sorted(dist_total, key=lambda x: x[1])[:10]

        return casos_similares_10

    def calculate_cosine_similarity(
        self, 
        user_to_recommend_normalized, 
        similar_cases
    ):

        # Calcular la distancia de Coseno
        distancias_coseno = []
        for index, row in similar_cases.iterrows():
            dist = cosine(user_to_recommend_normalized.values, row.values)
            distancias_coseno.append((index, dist))

        return distancias_coseno
    
    def calculate_hamming_distance(
        self, 
        user_to_recommend_normalized, 
        similar_cases
    ):
        # Calcular la distancia de Hamming
        distancias_hamming = []
        for index, row in similar_cases.iterrows():
            dist = hamming(user_to_recommend_normalized.values, row.values)
            distancias_hamming.append((index, dist))

        return distancias_hamming
    
    def calculate_combined_similarity(
        self, 
        casos_similares_coseno, 
        casos_similares_hamming,
        cluster = True
    ):
        # Ponderar las distancias
        distancia_total = []
        for i, (coseno_dist, hamming_dist) in enumerate(zip(casos_similares_coseno, casos_similares_hamming)):
            # Suponiendo que la distancia de Coseno es más importante
            dist_total = 0.5 * coseno_dist[1] + 0.5 * hamming_dist[1]
            distancia_total.append((i, dist_total)) if cluster else distancia_total.append((coseno_dist[0], dist_total))

        return distancia_total

    def recommend_10_similar_users(self):
        most_similar_cluster = self.get_most_similar_cluster()
        top_10_similar_cases = self.get_10_most_similar_cases(most_similar_cluster)

        return top_10_similar_cases

    