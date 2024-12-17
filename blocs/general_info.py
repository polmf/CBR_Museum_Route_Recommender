import streamlit as st
from helpers.ui_questions import ask_yes_or_no, ask_question_numerical, ask_question

def render():
    st.header("General Information")
    st.session_state.first_visit = ask_yes_or_no("Is this your first time visiting the museum?")
    st.session_state.visitas = 0 if st.session_state.first_visit else ask_question_numerical("How many times have you been here before?", 1, 10)
    st.session_state.companyia = ask_question("Who are you visiting the museum with?", ["Alone", "Group"])
    if st.session_state.companyia == "Group":
        st.session_state.group_size = ask_question_numerical("How many people are there in your group?", 2, 10)
    st.session_state.dies = ask_question_numerical("How many days are you planning on coming to the museum?", 1, 6)
    st.session_state.hores = ask_question_numerical("How many hours do you want to spend each day?", 1, 6)

