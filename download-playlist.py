import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import pyautogui

# --- LEER LA LISTA DESDE EL ARCHIVO JSON ---
try:
    with open('playlist_sample.json', 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)
        lista_canciones = datos["canciones"]
    print(f"Cargadas con éxito {len(lista_canciones)} canciones desde el archivo JSON.")
except FileNotFoundError:
    print("Error: No se encontró el archivo 'canciones.json'. Verifica la ruta.")
    exit()

# Inicializamos la variable de control y el índice de la lista
current_song = ""
indice = 0

# 2. Configurar el navegador
chrome_options = Options()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.maximize_window()

# El ciclo continuará hasta que current_song sea "siaca bo"
while current_song != "siaca bo":
    try:
        # Asignar el valor actual de la canción desde la lista
        current_song = lista_canciones[indice]
        print(f"\n--- Procesando canción actual: {current_song} ---")

        # --- PASO 1: BUSCAR LA CANCIÓN EN YOUTUBE ---
        driver.get("https://youtube.com")
        time.sleep(3)
        
        # Buscar usando la variable current_song
        busqueda = driver.find_element(By.NAME, "search_query")
        busqueda.clear()
        busqueda.send_keys(current_song)
        time.sleep(1)
        
        driver.find_element(By.CLASS_NAME, "ytSearchboxComponentSearchButton").click()
        time.sleep(3)
        
        link_element = driver.find_element(By.ID, "video-title")
        link_url = link_element.get_attribute("href")

        # --- PASO 2: IR A Y2MATE Y CONVERTIR ---
        driver.get("https://y2mate.gs")
        time.sleep(3)
        pestaña_principal = driver.current_window_handle

        driver.find_element(By.ID, "video").send_keys(link_url)
        time.sleep(2)
        
        boton = driver.find_element(By.XPATH, "//button[@type='submit']")
        boton.click()

        # Esperar y hacer clic en "Download"
        espera = WebDriverWait(driver, 30)
        boton_download = espera.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.download[type='button']"))
        )
        boton_download.click()
        
        # --- PASO 3: MANEJO DE PUBLICIDAD Y SISTEMA ---
        time.sleep(2)

        # Confirmar la descarga en la ventana del sistema
        pyautogui.press('enter')
        time.sleep(3) # Espera a que empiece la descarga real

        # Cerrar pestañas de publicidad intrusas
        todas_las_pestañas = driver.window_handles
        if len(todas_las_pestañas) > 1:
            for pestaña in todas_las_pestañas:
                if pestaña != pestaña_principal:
                    driver.switch_to.window(pestaña)
                    driver.close()
            driver.switch_to.window(pestaña_principal)

        print(f"Descarga iniciada con éxito para: {current_song}")

        # --- PASO 4: CONTROL DEL CICLO ---
        # Avanzamos el índice para la siguiente canción
        indice += 1
        
        # Si ya procesamos la última canción de la lista, forzamos el fin asignando "siaca bo"
        if indice >= len(lista_canciones):
            current_song = "siaca bo"
            print("\nSe ha descargado la última canción de la lista. Cambiando variable a 'siaca bo' para terminar.")
        else:
            # Si quedan más canciones, presionamos "Convert more" y continuamos el bucle
            boton_convert_more = espera.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.more[type='button']"))
            )
            boton_convert_more.click()
            time.sleep(2)

    except Exception as e:
        print(f"Ocurrió un error con la canción '{current_song}': {e}")
        # Si algo falla en una canción, intentamos pasar a la siguiente para no trabar el script por completo
        indice += 1
        if indice >= len(lista_canciones):
            current_song = "siaca bo"
        time.sleep(5)

# Fuera del bucle while
print("\nEl ciclo ha terminado correctamente.")
driver.quit()