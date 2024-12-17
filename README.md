# CBR Museum Route Recommender

# Proyecto de Recomendación en Museos

Este proyecto tiene como objetivo la creación de un sistema de recomendación para visitas a museos, basado en un enfoque de Casos Basados en Razón (CBR). El sistema recomienda rutas personalizadas a los visitantes del museo según sus preferencias, historial de visitas y conocimientos artísticos.

## Requisitos

Asegúrate de tener los siguientes paquetes instalados:

- Python 3.x
- Streamlit
- Jupyter Notebooks
- Bibliotecas adicionales (se mencionan a continuación)

## Instalación

1. **Clona el repositorio:**

   ```bash
   git clone <url-del-repositorio>
   ```
2. **Instala las dependencias:**

   Puedes instalar todas las dependencias necesarias utilizando `pip`:

   ```bash
   pip install -r requirements.txt
   ```
   
## Ejecución del Proyecto

Para ejecutar el proyecto, sigue estos pasos:
1.	**Ejecutar la aplicación web**:
  En la terminal, navega hasta el directorio del proyecto y ejecuta el siguiente comando para iniciar la aplicación:
   ```bash
   streamlit run main.py
   ```
  Esto abrirá automáticamente una página en tu navegador predeterminado y la aplicación comenzará a ejecutarse.
  
### Configuración Personalizada

Si deseas personalizar el sistema con casos iniciales o instancias personalizadas, sigue estos pasos:

1.	**Modificar los ficheros de configuración**:
Los archivos generacio_instancias.py y generacio_visitants.py están ubicados en la carpeta generacio. Modifica estos archivos para establecer los datos de instancias y visitantes según tus preferencias.
2.	**Ejecutar el análisis de casos**:
Abre y ejecuta el notebook analisi_casos.ipynb ubicado en la carpeta cbr_ciclo. Esto realizará el análisis de los casos y generará las instancias necesarias para el modelo.
3.	**Entrenar y guardar el modelo**:
Abre y ejecuta el notebook agent_model en la misma carpeta (cbr_ciclo). Esto entrenará un modelo basado en los datos configurados y lo guardará para su posterior uso.
4.	**Ejecutar el archivo principal**:
Una vez hayas completado los pasos anteriores, el sistema estará listo para funcionar. Vuelve a ejecutar el comando:
   ```bash
   streamlit run main.py
   ```

## Contribuidores
Miquel Ropero Serrano

Pol Margarit Fisas

Lola Monroy Mir

Lluc Furriols Llimargas

