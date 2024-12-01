import streamlit as st

def ask_yes_or_no(question):
    return st.radio(question, options=["Yes", "No"]) == "Yes"

def ask_question_numerical(question, min_value, max_value):
    return st.slider(question, min_value=min_value, max_value=max_value)

def ask_question(question, options):
    return st.radio(question, options=options)

def ask_multiple_options(question, options, limit):
    selected = st.multiselect(question, options=options)
    if len(selected) > limit:
        st.warning(f"You can select up to {limit} options.")
    return selected[:limit]
