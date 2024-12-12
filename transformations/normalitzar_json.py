import json
import os


def normalitzar_dades(input_file, output_file, camp_a_normalitzar):
    """
    Normalitza els valors dels camps especificats utilitzant Min-Max Scaling.
    
    :param input_file: Nom del fitxer JSON d'entrada.
    :param output_file: Nom del fitxer JSON de sortida.
    :param camp_a_normalitzar: Llista amb els noms dels camps a normalitzar.
    """
    # Llegeix el fitxer JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        dades = json.load(f)
    
    # Inicialitzar valors mínims i màxims per cada camp
    min_max_valors = {camp: {"min": float("inf"), "max": float("-inf")} for camp in camp_a_normalitzar}
    
    # Primer pas: Trobar els valors mínims i màxims per cada camp
    for registre in dades:
        for camp in camp_a_normalitzar:
            valor = registre[camp]
            if valor < min_max_valors[camp]["min"]:
                min_max_valors[camp]["min"] = valor
            if valor > min_max_valors[camp]["max"]:
                min_max_valors[camp]["max"] = valor
    
    # Segon pas: Aplicar Min-Max Scaling a cada camp
    for registre in dades:
        for camp in camp_a_normalitzar:
            valor = registre[camp]
            min_val = min_max_valors[camp]["min"]
            max_val = min_max_valors[camp]["max"]
            # Normalització: (valor - mínim) / (màxim - mínim)
            if max_val != min_val:  # Evitar divisió per zero
                registre[camp] = (valor - min_val) / (max_val - min_val)
            else:
                registre[camp] = 0.0  # Si màxim i mínim són iguals, assignem 0.0
    
    # Escriure el nou JSON amb les dades normalitzades
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dades, f, indent=4, ensure_ascii=False)
    
    print(f"Dades normalitzades i guardades a {output_file}")

# Camps a normalitzar
camps_a_normalitzar = [
    'visitant_edat',
    'visitant_visites',
    'visitant_dies',
    'visitant_hores',
    'visitant_coneixement',
    'visitant_quizz'
]

# Fitxers
fitxer_entrada = os.path.abspath('data/base_de_dades_final.json')
fitxer_sortida = os.path.abspath('data/base_dades_normalitzades.json')

# Normalitzar dades
normalitzar_dades(fitxer_entrada, fitxer_sortida, camps_a_normalitzar)