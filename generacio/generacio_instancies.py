import os
import pandas as pd
import json
import math
from classes import Quadre, Sala, Autor

def escalar_a_1_10(valor, min_valor, max_valor):
    if valor is None:
        return 1  # Valor per defecte
    return round(1 + (valor - min_valor) / (max_valor - min_valor) * 9, 2)

# Funció per calcular la complexitat
def calcular_complexitat(dim_cm2, any, estil):
    factor_dim = math.log(dim_cm2 + 1) if dim_cm2 else 0
    factor_any = max(0, (2024 - int(any)) / 100) if any and not pd.isna(any) else 0
    factors_estil = {"Surrealismo": 5, "Impressionisme": 4, "Renaixement": 6, "Modernisme": 3, "Abstracte": 4}
    factor_estil = factors_estil.get(estil, 2)
    complexitat_inicial = factor_dim + factor_any + factor_estil
    return complexitat_inicial

# Funció per calcular la rellevància
def calcular_relevancia(dim_cm2, any, estil):
    factor_dim = math.log(dim_cm2 + 1) if dim_cm2 else 0
    factor_any = max(0, (2024 - int(any)) / 50) if any and not pd.isna(any) else 0
    factors_estil = {"Surrealismo": 4, "Impressionisme": 5, "Renaixement": 7, "Modernisme": 3, "Abstracte": 4}
    factor_estil = factors_estil.get(estil, 2)
    rellevancia_inicial = factor_dim + factor_any + factor_estil
    return rellevancia_inicial

# Funció per assignar sales amb límit de quadres per sala
def assignar_sales(quadres, max_quadres_per_sala=200):
    sales = {}  # Diccionari per emmagatzemar les sales
    num_sala = 1  # Comptador per les sales

    for quadre in quadres:
        assignat = False  # Control per saber si s'ha assignat el quadre

        # Comprovar si el quadre es pot afegir a una sala existent amb el mateix estil
        for sala_id, sala in sales.items():
            # Comprovem si el quadre té el mateix estil i si la sala no ha superat el límit de quadres
            if sala.conte_estil == quadre.estil and len(sala.quadres) < max_quadres_per_sala:
                quadre.sala = sala_id  # Assignem la sala al quadre
                sala.afegir_quadre(quadre)  # Afegim el quadre a la sala
                assignat = True
                break

        # Si no s'ha assignat a cap sala existent, crear una nova sala
        if not assignat:
            nova_sala = Sala(sala=f"Sala {num_sala}", conte_estil=quadre.estil)
            quadre.sala = nova_sala.sala
            nova_sala.afegir_quadre(quadre)  # Afegim el quadre a la nova sala
            sales[nova_sala.sala] = nova_sala
            num_sala += 1
    return sales  # Retornem el diccionari de sales

# Processar la base de dades
def processar_base_dades(fitxer_csv, carpeta_desti):
    df = pd.read_csv(fitxer_csv)
    
    # Calcular complexitat i rellevància màximes i mínimes per normalitzar
    complexitats = []
    rellevancies = []

    for _, fila in df.iterrows():
        complexitat = calcular_complexitat(fila.get("Dim_cm2"), fila.get("Date"), fila.get("Style"))
        rellevancia = calcular_relevancia(fila.get("Dim_cm2"), fila.get("Date"), fila.get("Style"))
        complexitats.append(complexitat)
        rellevancies.append(rellevancia)

    # Valors màxims i mínims
    min_complexitat, max_complexitat = min(complexitats), max(complexitats)
    min_relevancia, max_relevancia = min(rellevancies), max(rellevancies)

    # Crear llistes de diccionaris per als quadres
    quadres = []
    autores = {}  # Diccionari per emmagatzemar els autors

    for _, fila in df.iterrows():
        complexitat_raw = calcular_complexitat(fila.get("Dim_cm2"), fila.get("Date"), fila.get("Style"))
        complexitat = escalar_a_1_10(complexitat_raw, min_complexitat, max_complexitat)

        rellevancia_raw = calcular_relevancia(fila.get("Dim_cm2"), fila.get("Date"), fila.get("Style"))
        rellevancia = escalar_a_1_10(rellevancia_raw, min_relevancia, max_relevancia)

        quadre = Quadre(
            nom=fila.get("Title"),
            dim_cm2=fila.get("Dim_cm2"),
            any=fila.get("Date"),
            autor=fila.get("Artist"),
            estil=fila.get("Style"),
            complexitat=complexitat,
            rellevancia=rellevancia,
            constituent_id=fila.get("ConstituentID")  # Afegim ConstituentID
        )
        quadres.append(quadre)

        # Crear instància d'Autor si l'autor no existeix en el diccionari
        autor_nom = fila.get("Artist")
        if autor_nom not in autores:
            autor = Autor(
                nom=autor_nom,
                #epoca=fila.get("Date"),  # Epoca és el mateix any en aquest exemple
                #estils=[fila.get("Style")],
                #nacionalitat=fila.get("Nationality"),
                #es_troba_a=fila.get("Museum")
            )
            autores[autor_nom] = autor
        else:
            autor = autores[autor_nom]
            if fila.get("Style") not in autor.estils:
                autor.estils.append(fila.get("Style"))

    # Assignar sales amb límit de quadres per sala
    sales = assignar_sales(quadres)

    # Guardar en JSON
    os.makedirs(carpeta_desti, exist_ok=True)
    
    # Guardar els quadres en un fitxer separat
    desti_fitxer_quadres = os.path.join(carpeta_desti, "quadres.json")
    with open(desti_fitxer_quadres, "w", encoding="utf-8") as f_json:
        # Convertir les instàncies de Quadre a diccionaris
        quadres_dict = [quadre.to_dict() for quadre in quadres]
        json.dump(quadres_dict, f_json, ensure_ascii=False, indent=4)

    # Guardar les sales en un fitxer separat
    desti_fitxer_sales = os.path.join(carpeta_desti, "sales.json")
    with open(desti_fitxer_sales, "w", encoding="utf-8") as f_json:
        # Convertir les instàncies de Sala a diccionaris
        sales_dict = {sala.sala: sala.to_dict() for sala in sales.values()}
        json.dump(sales_dict, f_json, ensure_ascii=False, indent=4)

    # Guardar els autors en un fitxer separat
    desti_fitxer_autors = os.path.join(carpeta_desti, "autors.json")
    with open(desti_fitxer_autors, "w", encoding="utf-8") as f_json:
        # Convertir les instàncies d'Autor a diccionaris
        autores_dict = {autor.nom: autor.to_dict() for autor in autores.values()}
        json.dump(autores_dict, f_json, ensure_ascii=False, indent=4)

    print(f"Instàncies guardades a: {desti_fitxer_quadres}, {desti_fitxer_sales} i {desti_fitxer_autors}")

# Crida a la funció principal
if __name__ == "__main__":
    fitxer_csv = "artworks_data/artworks_final.csv"
    carpeta_desti = "data"
    processar_base_dades(fitxer_csv, carpeta_desti)
