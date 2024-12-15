from generacio.classes import Visitant
from CBR_ciclo.Recuperar import Recuperar
from CBR_ciclo.Reutilizar import Reutilizar
from CBR_ciclo.Revisar import Revisar
from CBR_ciclo.Retener import Retener
import streamlit as st

def handle_cbr_process():
    # user_to_recommend = Visitant(
    #     visites=st.session_state.visitas,
    #     companyia=st.session_state.companyia,
    #     dies=st.session_state.dies,
    #     hores=st.session_state.hores,
    #     edat=st.session_state.edat,
    #     estudis=st.session_state.estudis,
    #     coneixements=st.session_state.coneixement,
    #     quizz=st.session_state.score,
    #     interessos_autor=st.session_state.interessos_autor,
    #     interessos_estils=st.session_state.interessos_estils,
    #     interessos_tipus=st.session_state.interessos_tipus
    # )

    user_to_recommend = Visitant(
        visites=1,
        companyia="alone",
        dies=1,
        hores=1,
        edat=30,
        estudis=True,
        coneixements=4,
        quizz=5,
        interessos_autor=["not-sure"],
        interessos_estils=["not-sure"]
    )


    recuperar = Recuperar(user_to_recommend)
    top_3_similar_users, most_similar_cluster = recuperar.recommend_3_similar_users()
    
    reutilizar = Reutilizar(user_to_recommend, top_3_similar_users)
    top_3_routes_recommended = reutilizar.recommend_routes()

    st.write("Estas son las rutas recomendadas para ti:")
    st.write(top_3_routes_recommended)

    # que el usuario escoja una ruta
    st.write("Por favor, selecciona una de las rutas recomendadas.")
    route_selected = st.selectbox("", top_3_routes_recommended)

    revisar = Revisar(user_to_recommend, route_selected)
    feedback = revisar.get_feedback()

    if st.button("Enviar Feedback"):
        retener = Retener(user_to_recommend, feedback, route_selected, most_similar_cluster)
        retener.eval_saving()
        st.success("¡Gracias por tu feedback! Se ha registrado correctamente.")
         
    # To do
    # if random.randint(0, 1) ==:
    #     agent_feedback = revisar.agent()
    #     retener = Retener(user_to_recommend, feedback, route_selected, agent_feedback)
    #     st.success("¡Gracias por tu feedback! Se ha registrado correctamente.")

handle_cbr_process()
