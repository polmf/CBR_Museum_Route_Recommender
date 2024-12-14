import pandas as pd
from transformations.functions import normalization

class Retener:
    """
    Guardar las rutas o visitantes con sus nuevos atributos modificados,
    para poder usarlos en el futuro.
    """
    # to do agent feedback
    def __init__(self, user_to_recommend, feedback, recommended_route, agent_feedback):
        self._base_de_casos = pd.read_csv("data/base_de_dades.csv")
        self._base_de_casos_normalized = pd.read_csv("data/base_de_casos_normalized.csv")
        self.user_to_recommend = self.user_to_df(user_to_recommend, recommended_route, feedback)
        self.user_to_recommend_normalized = normalization(user_to_recommend, self._base_de_casos)

    def user_to_df(self, user_to_recommend, recommended_route, feedback):
        """
        Convertir el objeto user_to_recommend a un DataFrame.
        """
        user_to_recommend = {
            'visitante_id': id,
            'visitant_edat': user_to_recommend.edat,
            'visitant_visites': user_to_recommend.visites,
            'visitant_dies': user_to_recommend.dies,
            'visitant_hores': user_to_recommend.hores,
            'visitant_companyia': user_to_recommend.companyia,
            'visitant_estudis': user_to_recommend.estudis,
            'visitant_coneixement': user_to_recommend.coneixements,
            'visitant_quizz': user_to_recommend.quizz,
            'visitant_interessos_autor': user_to_recommend.interessos_autor,
            'visitant_interessos_estils': user_to_recommend.interessos_estils,
            'ruta': recommended_route.nom,
            'ruta_quadres': recommended_route.quadres,
            'ruta_temps' : recommended_route.temps,
            'puntuacio_ruta': feedback,
            'puntuacio_agent': agent_feedback
        }

        return pd.DataFrame(user_to_recommend)
    
    def save_user_to_recommend(self):
        """
        Guardar el nuevo usuario en la base de datos.
        """
        self._base_de_casos = pd.concat([self._base_de_casos, self.user_to_recommend])
        self._base_de_casos.to_csv("data/base_de_casos.csv", index=False)

        self._base_de_casos_normalized = pd.concat([self._base_de_casos_normalized, self.user_to_recommend_normalized])
        self._base_de_casos_normalized.to_csv("data/base_de_casos_normalized.csv", index=False)

    def save_route_to_recommend(self):
        """
        Guardar la nueva ruta en la base de datos.
        """
        self._base_de_casos = pd.concat([self._base_de_casos, self.user_to_recommend])
        self._base_de_casos.to_csv("data/base_de_casos.csv", index=False)

        self._base_de_casos_normalized = pd.concat([self._base_de_casos_normalized, self.user_to_recommend_normalized])
        self._base_de_casos_normalized.to_csv("data/base_de_casos_normalized.csv", index=False)

    def save_all(self):
        """
        Guardar tanto el nuevo usuario como la nueva ruta en la base de datos.
        """
        self.save_user_to_recommend()
        self.save_route_to_recommend()
