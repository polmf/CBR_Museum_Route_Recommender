
import streamlit as st



def render():
    st.balloons()  # Animación de globos
    st.markdown(
        f"""
        <div style="
            background-color: #FFDD57; 
            padding: 2em; 
            border-radius: 15px; 
            text-align: center; 
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
            ">
            <h1 style="color: #333333; font-size: 3em;">🎉 Your Final Score: {st.session_state.score} / 6 🎉</h1>
            <p style="font-size: 1.5em; color: #555555;">Well done! Keep exploring the art world!</p>
        </div>
        """,
        unsafe_allow_html=True
    )   
    st.snow()  # Animación de nieve opcional        interests(df)  # Página 4: Interests