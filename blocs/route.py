import streamlit as st

def render():
    st.header("Ruta Final")
    st.write(st.session_state.estudis)
    