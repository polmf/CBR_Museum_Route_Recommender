import streamlit as st
from ui_blocks import render_block

def main_nou_cas():
    st.title("Museum Visitor Questionnaire")

    if "block" not in st.session_state:
        st.session_state.block = 1

    render_block(st.session_state.block)

    if st.session_state.block == 6:
        st.write("Thank you for completing the questionnaire!")

if __name__ == "__main__":
    main_nou_cas()
