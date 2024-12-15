import pandas as pd
import streamlit as st
import catboost

class Revisar:
    """
    Clase que representa la acción de revisar un caso.
    Recoger el feedback del usuario y, si no está satisfecho, realizar ajustes en las rutas futuras.
    """

    def __init__(self, user_to_recommend, route_selected):
        self.feedback = None
        self.user_to_recommend = user_to_recommend
        self.user_to_recommend_normalized = self.prepare_user_to_recommend()
        self.route_selected = route_selected
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
        
    def collect_user_feedback(self):
        """
        Recoge el feedback del usuario sobre la ruta recomendada.
        """
        st.write("¿Estás satisfecho con la ruta recomendada?")
        feedback = input("Introduce una puntuación del 1 al 5 a la ruta final recomendada (siendo 1 muy insatisfecho y 5 muy satisfecho): ")

        return feedback
    
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
        autors_ruta = self.get_authors_from_route()
        autors_user = self.user_to_recommend.interessos_autor

        estils_ruta = self.route_selected['estils']
        estils_user = self.user_to_recommend.interessos_estils
        
        objective_feedback = 0
        for autor in autors_ruta:
            if autor in autors_user:
                objective_feedback += 1
            
        for estil in estils_ruta:
            if estil in estils_user:
                objective_feedback += 1

        objective_feedback = (objective_feedback / (len(autors_ruta) + len(estils_ruta))) * 5

        # predict the feedback with the agent model
        agent_feedback = self.agent_model.predict(self.user_to_recommend_normalized)

        agent_feedback = (agent_feedback + objective_feedback) / 2

        
        return agent_feedback
    

    def get_feedback(self):
        """
        Obtiene el feedback del usuario y del agente.
        """
        user_feedback = self.collect_user_feedback()
        agent_feedback = self.define_agent_feedback()
        
        final_feedback = (user_feedback + agent_feedback) / 2

        return final_feedback