import streamlit as st
from helpers.ui_questions import ask_yes_or_no, ask_question_numerical

def render():
    st.header("Personal Background")
    if st.session_state.companyia == "Group":
        edat_group = 0
        for i in range(st.session_state.group_size):
            edat_group += ask_question_numerical(f"How old is person {i + 1} in the group?", 0, 110)
        st.session_state.edat = edat_group / st.session_state.group_size
    else:
        st.session_state.edat = ask_question_numerical("How old are you?", 0, 110)
    st.session_state.estudis = ask_yes_or_no("Have you studied any art-related subjects?")
    st.session_state.coneixement = ask_question_numerical("Rate your art knowledge (1-10):", 1, 10)


