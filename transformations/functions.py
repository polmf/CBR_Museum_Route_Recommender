from typing import List
import pandas as pd
from generacio.classes import Visitant

interessos_autor = [
    "ignacio-pinazo-camarlench", "fillol-granell-antonio", "federico-de-madrazo",
    "diego-rodriguez-de-silva-y-velazquez", "tiziano-vecellio", "joaquin-sorolla",
    "fiodor-rokotov", "peter-paul-rubens", "rembrandt-van-rijn", "pieter-bruegel-el-vell",
    "j-m-w-turner", "leonardo-da-vinci", "rosa-bonheur", "winslow-homer",
    "edouard-vuillard", "charles-burchfield", "ben-shahn", "sandro-botticelli",
    "salvador-dali", "edvard-munch", "edouard-manet", "hieronymus-bosch",
    "johannes-vermeer", "eugene-delacroix", "not-sure"
]

interessos_estils = [
    "modernisme", "romanticisme", "barroc", "renaixement", "impressionisme",
    "realisme", "contemporani", "surrealisme", "expressionisme", "not-sure"
]

companyia = ["alone", "couple", "family", "group"]

def convert_cat_cols_new_user(
    user_to_recommend: Visitant,
    interessos_autor: List[str] = interessos_autor,
    interessos_estils: List[str] = interessos_estils,
    companyia: List[str] = companyia,
) -> pd.DataFrame:
    """
    Convertim l'objecte user_to_recommend a un df per poder comparar-lo amb la base de dades.
    """ 
    visitant = {
        'visitant_edat': user_to_recommend.edat,
        'visitant_dies': user_to_recommend.dies,
        'visitant_visites': user_to_recommend.visites,
        'visitant_hores': user_to_recommend.hores,
        'visitant_estudis': user_to_recommend.estudis,
        'visitant_coneixement': user_to_recommend.coneixements,
        'visitant_quizz': user_to_recommend.quizz,
    }

    for autor in interessos_autor:
        visitant[f'autor_{autor}'] = 1 if autor in user_to_recommend.interessos_autor else 0
    
    for estil in interessos_estils:
        visitant[f'estil_{estil}'] = 1 if estil in user_to_recommend.interessos_estils else 0

    for companyia in companyia:
        visitant[f'companyia_{companyia}'] = 1 if companyia in user_to_recommend.companyia else 0

    visitant['visitant_estudis'] = 1 if visitant['visitant_estudis'] else 0

    return pd.DataFrame([visitant])
    
def normalization(
    user_to_recommend: Visitant,
    base_de_casos: pd.DataFrame,
    num_cols_to_compare: List[str] = [
        'visitant_edat',
        'visitant_visites',
        'visitant_dies',
        'visitant_hores',
        'visitant_coneixement',
        'visitant_quizz',
    ],
) -> pd.DataFrame:
    
    user_to_recommend = convert_cat_cols_new_user(user_to_recommend)
    
    for col in num_cols_to_compare:
        max_value = base_de_casos[col].max()
        min_value = base_de_casos[col].min()

        user_to_recommend[col] = (user_to_recommend[col] - min_value) / (max_value - min_value)

    return user_to_recommend

def calcul_temps_quadre(
    visitant: Visitant,
    quadre: str,
    quadres: pd.DataFrame,
):
    pass