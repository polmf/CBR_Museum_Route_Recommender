import streamlit as st
from helpers.ui_questions import ask_yes_or_no, ask_question_numerical

def render():
    st.header("Personal Background")
    st.session_state.edat = ask_question_numerical("How old are you?", 0, 110)
    st.session_state.estudis = ask_yes_or_no("Have you studied any art-related subjects?")
    st.session_state.coneixement = ask_question_numerical("Rate your art knowledge (1-10):", 1, 10)


