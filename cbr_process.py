from generacio.classes import Visitant
from CBR_ciclo.Recuperar import Recuperar
from CBR_ciclo.Reutilizar import Reutilizar
from CBR_ciclo.Revisar import Revisar
from CBR_ciclo.Retener import Retener
import random 
import streamlit as st

# with open('data/quadres.json', 'r', encoding='utf-8') as f_quadres:
#         quadres_data = json.load(f_quadres)
#         quadres = [Quadre.from_dict(data) for data in quadres_data]

#     # Leer y convertir el archivo de las sales
#     with open('data/sales.json', 'r', encoding='utf-8') as f_sales:
#         sales_data = json.load(f_sales)
#         sales = {sala_id: Sala.from_dict(data) for sala_id, data in sales_data.items()}

#     # Leer y convertir el archivo de los autores
#     with open('data/autors.json', 'r', encoding='utf-8') as f_autores:
#         autores_data = json.load(f_autores)
#         autors = {autor_nom: Autor.from_dict(data) for autor_nom, data in autores_data.items()}

def handle_cbr_process():
    # user_to_recommend = Visitant(
    #     visites=st.session_state.visitas,
    #     companyia=st.session_state.companyia,
    #     dies=st.session_state.dies,
    #     hores=st.session_state.hores,
    #     edat=st.session_state.edat,
    #     estudis=st.session_state.estudis,
    #     coneixement=st.session_state.coneixement,
    #     quizz=st.session_state.score,
    #     interessos_autor=st.session_state.interessos_autor,
    #     interessos_estils=st.session_state.interessos_estils
    # )

    user_to_recommend = Visitant(
        visites=1,
        companyia="alone",
        dies=1,
        hores=2,
        edat=25,
        estudis=False,
        coneixement=6,
        quizz=3,
        interessos_autor="not-sure",
        interessos_estils="not-sure"
    )

    recuperar = Recuperar(user_to_recommend)
    top_3_similar_users = recuperar.recommend_3_similar_users()
    
    reutilizar = Reutilizar(user_to_recommend, top_3_similar_users)
    top_3_routes_recommended = reutilizar.recommend_routes()

    st.write("Estas son las rutas recomendadas para ti:")
    st.write(top_3_routes_recommended)

    # que el usuario escoja una ruta
    st.write("Por favor, selecciona una de las rutas recomendadas.")
    route_selected = st.selectbox("", top_3_routes_recommended)

    revisar = Revisar()
    feedback = revisar.collect_feedback()

    if st.button("Enviar Feedback"):
        retener = Retener(user_to_recommend, feedback, route_selected)
        st.success("¡Gracias por tu feedback! Se ha registrado correctamente.")
        
    # To do
    # if random.randint(0, 1) ==:
    #     agent_feedback = revisar.agent()
    #     retener = Retener(user_to_recommend, feedback, route_selected, agent_feedback)
    #     st.success("¡Gracias por tu feedback! Se ha registrado correctamente.")


handle_cbr_process()