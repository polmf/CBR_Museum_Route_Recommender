from CBR_ciclo.Recuperar import Recuperar
from CBR_ciclo.Reutilizar import Reutilizar
from CBR_ciclo.Revisar import Revisar
from CBR_ciclo.Retener import Retener
import streamlit as st

def cbr_recuperar_reutilizar():

    recuperar = Recuperar(st.session_state.user_to_recommend)
    top_3_similar_users, most_similar_cluster = recuperar.recommend_3_similar_users()
    
    reutilizar = Reutilizar(st.session_state.user_to_recommend, top_3_similar_users)
    top_3_routes_recommended = reutilizar.recommend_routes()
    
    return top_3_routes_recommended, most_similar_cluster

def cbr_revisar_retener():

    revisar = Revisar(
        st.session_state.user_to_recommend, 
        st.session_state.ruta_completa, 
        st.session_state.evaluation,
        st.session_state.most_similar_cluster
    )
    feedback = revisar.get_feedback()

    print("Ruta completa:", st.session_state.ruta_completa)

    retener = Retener(st.session_state.user_to_recommend, feedback, st.session_state.ruta_completa, st.session_state.most_similar_cluster)
    retener.eval_saving()
    st.success("¡Gracias por tu feedback! Se ha registrado correctamente.")
         
    # To do
    # if random.randint(0, 1) ==:
    #     agent_feedback = revisar.agent()
    #     retener = Retener(user_to_recommend, feedback, route_selected, agent_feedback)
    #     st.success("¡Gracias por tu feedback! Se ha registrado correctamente.")

#handle_cbr_process()
