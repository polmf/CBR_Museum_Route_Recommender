import streamlit as st

class Revisar:
    """
    Clase que representa la acción de revisar un caso.
    Recoger el feedback del usuario y, si no está satisfecho, realizar ajustes en las rutas futuras.
    """

    def __init__(self):
        self.feedback = None
        
    def collect_feedback(self):
        """
        Recoge el feedback del usuario sobre la ruta recomendada.
        """
        st.write("¿Estás satisfecho con la ruta recomendada?")
        feedback = input("Introduce una puntuación del 1 al 5 a la ruta final recomendada (siendo 1 muy insatisfecho y 5 muy satisfecho): ")

        
        return feedback
    

    def agent():
        """
        Método que representa la acción de revisar un caso.
        """
        # To do

        return feedback