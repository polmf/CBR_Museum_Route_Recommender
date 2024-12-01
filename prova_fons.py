import streamlit as st
import base64
import os

[theme]
base="dark"


# Función para cargar la imagen y convertirla a Base64
def set_background(image_file):
    # Comprobar si el archivo existe
    if not os.path.exists(image_file):
        st.error(f"El archivo {image_file} no se encuentra. Verifica la ruta.")
        return

    # Leer la imagen local
    with open(image_file, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode()

    # Crear el CSS para el fondo
    css_code = f"""
    <style>
    body {{
        background-image: url("data:image/jpeg;base64,{base64_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    # Aplicar el CSS
    st.markdown(css_code, unsafe_allow_html=True)

# Cambiar la ruta al archivo local según corresponda
set_background(r"C:\Users\USER\OneDrive - Universitat Politècnica de Catalunya\Escritorio\UPC\cinquequatri\SBC\SBC_2\fondo.jpg")
 # Ajusta la ruta al archivo

st.title("¡Prueba de fondo!")
st.write("Si ves el fondo, el código funciona correctamente.")
