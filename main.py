"""
Hecho por: Lluc Furriols, Pol Margarit, Miquel Ropero y Lola Monroy
Copyright 2024

Fichero principal del proyecto
"""

from CBR_ciclo.Recuperar import Recuperar
from CBR_ciclo.Reutilizar import Reutilizar
from CBR_ciclo.Revisar import Revisar
from CBR_ciclo.Retener import Retener

from generacio.recom_clips import gather_visitor_info

# Datos del nuevo usuario
# Obtenemos estos datos mediante un formulario o una interfaz de usuario dado por recom_clips.py

user_to_recommend = gather_visitor_info()

# Fase de Recuperar
# Buscamos casos similares en la base de casos
recuperar = Recuperar(user_to_recommend)
top_5_similar_users = recuperar.recommend_similar_users(user_to_recommend)
routes_of_similar_users = recuperar.get_routes_of_similar_users(top_5_similar_users)


# Fase de Reutilizar
# Adaptamos el caso más similar a las necesidades del nuevo usuario
reutilizar = Reutilizar(user_to_recommend=user_to_recommend, top_5_similar_users=top_5_similar_users)
route_selected = reutilizar.get_route_more_repeated_from_similar_cases()
route_adjusted = reutilizar.adjust_route_to_user_preferences(route_selected)


# Fase de Revisar
# Recogemos el feedback del usuario sobre la recomendación
revisar = Revisar(route_adjusted)
revisar.print_routes()
feedback = revisar.collect_feedback()


# Fase de Retener
# Guardamos el nuevo caso en la base de casos para futuras recomendaciones
retener = Retener(user_to_recommend, feedback)