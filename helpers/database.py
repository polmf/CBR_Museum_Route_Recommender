import pandas as pd

def load_database():
    df = pd.read_csv("artworks_data/artworks_final.csv")
    return df
