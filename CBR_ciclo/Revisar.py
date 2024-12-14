import streamlit as st

class Revisar:
    """
    Clase que representa la acción de revisar un caso.
    Recoger el feedback del usuario y, si no está satisfecho, realizar ajustes en las rutas futuras.
    """

    def __init__(self, user_to_recommend, route_selected):
        self.feedback = None
        self.user_to_recommend = user_to_recommend
        self.route_selected = route_selected
        
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
        
        agent_feedback = 0
        for autor in autors_ruta:
            if autor in autors_user:
                agent_feedback += 1
            
        for estil in estils_ruta:
            if estil in estils_user:
                agent_feedback += 1

        agent_feedback = agent_feedback / (len(autors_ruta) + len(estils_ruta))

        # es podria tmb utilitzar una xarxa neuronal per predir el feedback de l'usuari i
        # si es diferencia molt del feedback de l'agent, es podria considerar un outlier
        # i per tant, no tenir en compte el feedback de l'usuari
        
        return agent_feedback
    

    def get_feedback(self):
        """
        Obtiene el feedback del usuario y del agente.
        """
        user_feedback = self.collect_user_feedback()
        agent_feedback = self.define_agent_feedback()
        
        final_feedback = (user_feedback + agent_feedback) / 2

        return final_feedback