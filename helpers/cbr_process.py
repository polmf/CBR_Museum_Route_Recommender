import random

import pandas as pd
from CBR_ciclo.Recuperar import Recuperar
from CBR_ciclo.Reutilizar import Reutilizar
from CBR_ciclo.Revisar import Revisar
from CBR_ciclo.Retener import Retener
import streamlit as st
from transformations.functions import clean_old_cases

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
    #st.success("¡Gracias por tu feedback! Se ha registrado correctamente.")
         
    # To do oblit de casos
    # entrar en el if 1 de cada 10000 vegades
    if random.randint(1, 10000) == 1:
        # Cargar las bases de datos
        base_de_casos = pd.read_json("data/base_de_dades_final.json")
        base_de_casos_normalized = pd.read_csv("data/base_de_dades_normalized.csv")
        
        # Limpiar los casos antiguos de la base sin normalizar
        casos_eliminados = clean_old_cases(base_de_casos)
        
        # Eliminar los mismos casos en la base normalizada usando los índices
        base_de_casos_actualizada = base_de_casos.drop(casos_eliminados.index)
        base_de_casos_normalized_actualizada = base_de_casos_normalized.drop(casos_eliminados.index)
        
        # Guardar las bases de datos actualizadas
        base_de_casos_actualizada.to_json("data/base_de_dades_final.json", orient="records", lines=False)
        base_de_casos_normalized_actualizada.to_csv("data/base_de_dades_final_normalized.csv", index=False, header=True)
        
        # Mostrar resultados (si se ejecuta en Streamlit o consola)
        print("Limpieza completada.")
        print(f"Casos eliminados (JSON): {len(casos_eliminados)}")
        print(f"Casos eliminados (CSV): {len(casos_eliminados)}")


