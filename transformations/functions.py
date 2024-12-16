from typing import List, Tuple
import numpy as np
import pandas as pd
from sklearn.metrics import jaccard_score
from sklearn.metrics.pairwise import cosine_similarity
from generacio.classes import Visitant
from sklearn.preprocessing import MultiLabelBinarizer

artworks_data = pd.read_csv("artworks_data/artworks_final.csv")

interessos_estils = artworks_data['Style'].unique().tolist()

companyia = [
    "alone", "group"
]

interessos_types = artworks_data['Classification'].unique().tolist()

def convert_cat_cols_user(
    user: pd.DataFrame,
) -> pd.DataFrame:
    
    for estil in interessos_estils:
        user[f'estil_{estil}'] = user['visitant_interessos_estils'].apply(
            lambda x: 1 if estil.lower() in [elem.lower() for elem in x] else 0
        )

    # Creem una columna binària per cada companyia
    for comp in companyia:
        user[f'companyia_{comp}'] = user['visitant_companyia'].apply(
            lambda x: 1 if comp.lower() in [elem.lower() for elem in x] else 0
        )

    # Creem una columna binària per cada tipus d'interès
    for tipus in interessos_types:
        user[f'interes_{tipus}'] = user['visitant_interessos_tipus'].apply(
            lambda x: 1 if tipus.lower() in [elem.lower() for elem in x] else 0
        )

    # convertim la columna visitant_estudis a binaria
    user['visitant_estudis'] = user['visitant_estudis'].apply(lambda x: 1 if x else 0)

    user = user.drop(columns=['visitant_interessos_estils', 'visitant_interessos_autor', 
                                      'visitant_companyia', 'visitant_interessos_tipus'])

    return user

def normalize(
    user: pd.DataFrame,
    base_de_casos: pd.DataFrame
) -> pd.DataFrame:
    
    user = convert_cat_cols_user(user)
    
    print('cols base de casos: ', base_de_casos.columns)

    cols_to_compare = base_de_casos.select_dtypes(include=['int64', 'float']).columns.to_list()
    cols_to_compare.remove('puntuacio_ruta')
    cols_to_compare.remove('visitante_id')
    cols_to_compare.remove('ruta_temps')
    cols_to_compare.remove('cluster')
    cols_to_compare.remove('recompte_utilitzat')

    for col in cols_to_compare:
        max_value = base_de_casos[col].max()
        min_value = base_de_casos[col].min()

        user[col] = (user[col] - min_value) / (max_value - min_value)

    return user


def user_to_pd(user_to_recommend: Visitant) -> pd.DataFrame:
    """
    Convertir un objecte Visitant a un DataFrame de Pandas.
    """
    user_dict = {
        "visitant_visites": user_to_recommend.visites,
        "visitant_companyia": user_to_recommend.companyia,
        "visitant_dies": user_to_recommend.dies,
        "visitant_hores": user_to_recommend.hores,
        "visitant_edat": user_to_recommend.edat,
        "visitant_estudis": user_to_recommend.estudis,
        "visitant_coneixement": user_to_recommend.coneixements,
        "visitant_quizz": user_to_recommend.quizz,
        "visitant_interessos_autor": user_to_recommend.interessos_autor,
        "visitant_interessos_estils": user_to_recommend.interessos_estils,
        "visitant_interessos_tipus": user_to_recommend.interessos_tipus,
    }

    return pd.DataFrame(user_dict, index=[0])


def is_case_redundant(
    similarities_user: List[Tuple[int, float]],
    similarities_ruta: List[Tuple[int, float]],
    feedback_differences: List[float],
    user_sim_threshold: float = 0.9,
    route_sim_threshold: float = 0.8,
    feedback_diff_threshold: float = 0.5
) -> bool:
    """
    Comprova si un cas és redundant amb els casos existents.
    """
    
    for (idx_user, similarity_user), (idx_ruta, similarity_ruta) in zip(similarities_user, similarities_ruta):
        # Comprueba si el caso es redundante
        if (similarity_user > user_sim_threshold and
            similarity_ruta > route_sim_threshold and
            feedback_differences[idx_user] < feedback_diff_threshold):
            return True  # El caso es redundante
    return False  # El caso aporta valor


def mesura_utilitat(
    casos: pd.DataFrame,
    most_similar_cluster: int,
    user_to_recommend: pd.DataFrame,
    route_selected: pd.DataFrame,
    feedback: float
    ) -> pd.DataFrame:
    """
    Aquesta funció calcula la utilitat dels casos que tenim.

    :param casos: DataFrame amb els casos que tenim
    :return: DataFrame amb la utilitat de cada cas
    """
    # get the cases from the most similar cluster
    casos = casos[casos['cluster'] == most_similar_cluster]

    # Extraer los cuadros y convertirlos a representación binaria
    mlb = MultiLabelBinarizer()
    cuadros_encoded = mlb.fit_transform(casos['ruta_quadres_list'])

    route_selected_encoded = mlb.transform([route_selected['quadres']])

    # Calcular la similitud Jaccard con las rutas existentes
    similarities_ruta = []
    for idx, ruta_vector in enumerate(cuadros_encoded):  # Usar índices de `casos`
        similarity = jaccard_score(route_selected_encoded[0], ruta_vector)
        similarities_ruta.append((idx, similarity))

    # calcular la similitud de los casos con el usuario
    user_to_recommend_df = user_to_pd(user_to_recommend)
    user_to_recommend_normalized = normalize(user_to_recommend_df, casos)
    similarities_user = []
    for idx, (index, cas) in enumerate(casos.iterrows()):
        cas_normalized = normalize(cas.to_frame().T, casos)
        cas_normalized = cas_normalized[user_to_recommend_normalized.columns]
        similarity = cosine_similarity(user_to_recommend_normalized, cas_normalized)
        similarities_user.append((idx, similarity[0][0]))  # Acceso al valor escalar

    # Calcular la diferencia de feedback
    feedback_differences = np.abs(casos['puntuacio_ruta'] - feedback)

    # Calcular la utilidad
    return not is_case_redundant(
        similarities_user, similarities_ruta, feedback_differences
        )

    
