import pandas as pd

class Retener:
    """
    Guardar las rutas o visitantes con sus nuevos atributos modificados,
    para poder usarlos en el futuro.
    """

    def __init__(self, user_to_recommend, feedback):
        self._base_de_casos = pd.read_csv("data/base_de_dades.csv")
        self.add_feedback(user_to_recommend, feedback)
        self.save_case(user_to_recommend)

    def add_feedback(self, user_to_recommend, feedback):
        """
        Añade el feedback del usuario a la base de casos.
        """
        user_to_recommend.feedback = feedback

    def save_case(self, case):
        """
        Guarda un nuevo caso en la base de casos.
        """
        case_data = vars(case) 

        self._base_de_casos = pd.concat(
            [self._base_de_casos, pd.DataFrame([case_data])], 
            ignore_index=True
        )

        #self._base_de_casos.to_csv("data/base_de_dades.csv", index=False)
