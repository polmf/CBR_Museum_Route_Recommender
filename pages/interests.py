import streamlit as st
from helpers.ui_questions import ask_multiple_options

def render(df):
    st.header("Interests")
    options_autor = df["Artist"].dropna().unique().tolist()
    options_estils = df["Style"].dropna().unique().tolist()
    options_type = df["Classification"].dropna().unique().tolist()

    st.session_state.interessos_autor = ask_multiple_options("Select up to 3 artists", options_autor, 3)
    st.session_state.interessos_estils = ask_multiple_options("Select up to 3 styles", options_estils, 3)
    st.session_state.interessos_tipus = ask_multiple_options("Select up to 3 art types", options_type, 3)

