import streamlit as st
from ui_blocks import render_block
from cbr_process import handle_cbr_process

def main_nou_cas():
    st.title("Museum Visitor Questionnaire")

    if "block" not in st.session_state:
        st.session_state.block = 1

    render_block(st.session_state.block)

    if st.session_state.block == 5:
        handle_cbr_process()

if __name__ == "__main__":
    main_nou_cas()
