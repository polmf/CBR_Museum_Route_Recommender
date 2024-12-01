from generacio.classes import Visitant
from CBR_ciclo.Recuperar import Recuperar
from CBR_ciclo.Reutilizar import Reutilizar
from CBR_ciclo.Revisar import Revisar
from CBR_ciclo.Retener import Retener
import streamlit as st

def handle_cbr_process():
    user_to_recommend = Visitant(
        visites=st.session_state.visitas,
        companyia=st.session_state.companyia,
        dies=st.session_state.dies,
        hores=st.session_state.hores,
        edat=st.session_state.edat,
        estudis=st.session_state.estudis,
        coneixement=st.session_state.coneixement,
        quizz=st.session_state.score,
        interessos_autor=st.session_state.interessos_autor,
        interessos_estils=st.session_state.interessos_estils
    )

    recuperar = Recuperar(user_to_recommend)
    top_5_similar_users = recuperar.recommend_similar_users(user_to_recommend)
    reutilizar = Reutilizar(user_to_recommend, top_5_similar_users)
    route_selected = reutilizar.get_route_more_repeated_from_similar_cases()

    revisar = Revisar(route_selected)
    ruta = revisar.print_routes()
    st.write("Estas son las rutas recomendadas para ti:")
    st.write(ruta)

    feedback = st.slider("Introduce una puntuación del 1 al 5 a la ruta recomendada", 1, 5)
    if st.button("Enviar Feedback"):
        retener = Retener(user_to_recommend, feedback)
        st.success("¡Gracias por tu feedback! Se ha registrado correctamente.")