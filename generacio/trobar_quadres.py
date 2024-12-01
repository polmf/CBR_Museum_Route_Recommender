from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Configura el driver de Chrome
service = Service('ruta/a/chromedriver')  # Descarga ChromeDriver y especifica su ruta
driver = webdriver.Chrome(service=service)

# Navega a la página
driver.get("https://artsandculture.google.com/category/art-movement")

# Encuentra los elementos
movements = driver.find_elements(By.CLASS_NAME, 'item-class')  # Reemplaza 'item-class' con la clase correcta

# Extraer enlaces y nombres
for movement in movements:
    name = movement.text.strip()
    link = movement.get_attribute('href')
    print(f"Movimiento: {name}, Link: {link}")

# Cierra el navegador
driver.quit()
