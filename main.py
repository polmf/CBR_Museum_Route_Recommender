import streamlit as st
from ui_blocks import render_block
import pandas as pd

def load_database():
    df = pd.read_csv("artworks_data/artworks_final.csv")
    return df

# Función auxiliar para obtener valores únicos de una columna
def get_unique_options(df, column_name):
    return df[column_name].dropna().unique().tolist()

def main_nou_cas():
    
    df = load_database()

    options_autor = get_unique_options(df, "Artist")
    options_estils = get_unique_options(df, "Style")
    options_type = get_unique_options(df, "Classification")
    
    st.title("Museum Visitor Questionnaire")

    if "block" not in st.session_state:
        st.session_state.block = 1

    render_block(st.session_state.block, options_autor, options_estils, options_type)

    if st.session_state.block == 6:
        st.write("Thank you for completing the questionnaire!")

if __name__ == "__main__":
    main_nou_cas()
