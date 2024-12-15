import pandas as pd
import streamlit as st
import catboost

class Revisar:
    """
    Clase que representa la acción de revisar un caso.
    Recoger el feedback del usuario y, si no está satisfecho, realizar ajustes en las rutas futuras.
    """

    def __init__(self, user_to_recommend, route_selected, feedback):
        self.feedback = None
        self.user_to_recommend = user_to_recommend
        self.user_to_recommend_normalized = self.prepare_user_to_recommend()
        self.route_selected = route_selected
        self.user_feedback = feedback
        self.agent_model = catboost.CatBoostRegressor()
        self.agent_model.load_model('CBR_ciclo/agent_model/best_catboost_model.cb')

    def prepare_user_to_recommend(self):

        temps_total = self.user_to_recommend.dies * 24 + self.user_to_recommend.hores

        # convert user_to_recommend to a DataFrame
        user_to_recommend = {
            'visitant_edat': self.user_to_recommend.edat,
            'visitant_visites': self.user_to_recommend.visites,
            'visitant_temps_total': temps_total,
            'visitant_companyia': self.user_to_recommend.companyia,
            'visitant_estudis': self.user_to_recommend.estudis,
            'visitant_coneixement': self.user_to_recommend.coneixements,
            'visitant_quizz': self.user_to_recommend.quizz,
            'visitant_interessos_estils': self.user_to_recommend.interessos_estils,
            'visitant_interessos_tipus': self.user_to_recommend.interessos_tipus,
        }

        user_to_recommend = pd.DataFrame(user_to_recommend)

        user_to_recommend['visitant_interessos_estils'] = user_to_recommend['visitant_interessos_estils'].apply(
            lambda x: x[0] if isinstance(x, list) else x)
        
        user_to_recommend['visitant_interessos_tipus'] = user_to_recommend['visitant_interessos_tipus'].apply(
            lambda x: x[0] if isinstance(x, list) else x)
        
        return user_to_recommend
        
    
    def get_authors_from_route(self):
        """
        Obtiene los autores de las rutas recomendadas.
        """
        quadres = self.route_selected['quadres']
        autors = []
        for quadre in quadres:
            autor = quadre['autor']
            autors.append(autor)
        
        return autors
    
    def define_agent_feedback(self):
        """
        Define el feedback del agente.
        """
        # predict the feedback with the agent model
        agent_feedback = self.agent_model.predict(self.user_to_recommend_normalized)

        return agent_feedback
    

    def get_feedback(self):
        """
        Obtiene el feedback del usuario y del agente.
        """
        agent_feedback = self.define_agent_feedback()
        
        final_feedback = (self.user_feedback + agent_feedback) / 2

        return final_feedback