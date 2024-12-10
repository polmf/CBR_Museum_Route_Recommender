"""
Aquest mòdul conté la funció mesura_utilitat que calcula la utilitat 
dels casos que tenim.
"""
import pandas as pd
from utils import Dataframe
from datetime import timestamp

base_casos = pd.read_csv('data/base_de_dades.csv')

def mesura_utilitat(casos: pd.DataFrame) -> pd.DataFrame:
    """
    Aquesta funció calcula la utilitat dels casos que tenim.

    :param casos: DataFrame amb els casos que tenim
    :return: DataFrame amb la utilitat de cada cas
    """
    # Data thresholds and calculations
    data_actual = pd.Timestamp.today()
    data_threshold = data_actual - pd.Timedelta(days=95)

    # Vectorized conditions
    valid_dates = casos['ultima_vegada'] >= data_threshold
    high_reuse = casos['num_reutilitzacions'] > 5
    valid_feedback = (casos['puntuacio_ruta'] == 1) or (casos['puntuacio_ruta'] == 5)

    # Apply conditions
    util_cases = casos[valid_dates & high_reuse & valid_feedback]

    return util_cases

        
