import pandas as pd
from transformations.functions import normalize, mesura_utilitat, user_to_pd

class Retener:
    """
    Guardar las rutas o visitantes con sus nuevos atributos modificados,
    para poder usarlos en el futuro.
    """
    def __init__(self, user_to_recommend, feedback, recommended_route, most_similar_cluster):
        self.base_de_casos = pd.read_json("data/base_de_dades_final.json")
        self.base_de_casos_normalized = pd.read_csv("data/base_de_dades_normalized.csv")

        self.user_to_recommend = user_to_recommend
        user_to_recommend = user_to_pd(user_to_recommend)
        self.user_to_recommend_normalized = normalize(user_to_recommend, self.base_de_casos)

        self.feedback = feedback
        self.recommended_route = recommended_route
        self.most_similar_cluster = most_similar_cluster

    def eval_saving(self):
        """
        Evaluar si se guarda el caso o no.
        """
        if mesura_utilitat(
            self.base_de_casos,
            self.most_similar_cluster,
            self.user_to_recommend,
            self.recommended_route,
            self.feedback
        ):
            self.save_user_to_recommend()
        
        return True
        
    def save_user_to_recommend(self):
        """
        Guardar el usuario recomendado.
        """
        self.user_to_recommend = user_to_pd(self.user_to_recommend)

        self.user_to_recommend['puntuacio_ruta'] = self.feedback
        self.user_to_recommend['ruta'] = self.recommended_route['ruta']
        self.user_to_recommend['ruta_quadres_list'] = [self.recommended_route['quadres']]
        self.user_to_recommend['ruta_temps'] = self.recommended_route['temps']
        self.user_to_recommend['cluster'] = self.most_similar_cluster
        self.user_to_recommend['visitante_id'] = self.base_de_casos['visitante_id'].max() + 1
        self.user_to_recommend['recompte_utilitzat'] = 1
        self.user_to_recommend['data_ultim_us'] = pd.Timestamp.now().strftime("%Y-%m-%d")

        self.user_to_recommend['ruta_quadres'] = [
            self.recommended_route['ruta_quadres']
        ] if len(self.recommended_route['ruta_quadres']) > 1 else self.recommended_route['ruta_quadres']
        
        self.user_to_recommend_normalized['cluster'] = self.most_similar_cluster

        self.base_de_casos = pd.concat([self.base_de_casos, self.user_to_recommend], ignore_index=True)
        self.base_de_casos.to_json("data/base_de_dades_final.json", orient="records", lines=False)
        
        self.base_de_casos_normalized = pd.concat([self.base_de_casos_normalized, self.user_to_recommend_normalized], ignore_index=True)
        self.base_de_casos_normalized.to_csv("data/base_de_dades_final_normalized.csv", index=False, header=True)

        return True
