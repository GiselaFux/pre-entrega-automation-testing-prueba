#  utils/helpers.py — Funciones 
# os es un módulo estándar de Python para interactuar con el sistema operativo.
#time se usa para manejar tiempos y pausas
import os
import time
#By es una clase de Selenium que define las formas de localizar elementos en la página.
from selenium.webdriver.common.by import By
#WebDriverWait permite hacer esperas explícitas hasta que se cumpla una condición, en lugar de usar time.sleep fijo.
from selenium.webdriver.support.ui import WebDriverWait
#expected_conditions (alias EC) contiene muchas funciones que describen condiciones que esperamos que se cumplan en la página
from selenium.webdriver.support import expected_conditions as EC
#TimeoutException es una excepción de Selenium que se lanza cuando se agota el tiempo de espera en un WebDriverWait y la condicion no se cumple
from selenium.common.exceptions import TimeoutException
 
 
# --- Constantes del sitio ---
URL_BASE       = "https://www.saucedemo.com"
URL_INVENTARIO = "https://www.saucedemo.com/inventory.html"
URL_CARRITO    = "https://www.saucedemo.com/cart.html"
 
# Credenciales de prueba provistas por SauceDemo
USUARIO_VALIDO   = "standard_user"
PASSWORD_VALIDO  = "secret_sauce"
 
# Tiempo máximo de espera explícita (en segundos)
TIMEOUT = 10
 
 
# ============================================================
#  Funciones de Login
# ============================================================
 
def realizar_login(driver, usuario=USUARIO_VALIDO, password=PASSWORD_VALIDO):
    """
    Navega a la página de login e ingresa las credenciales dadas.
 
    Args:
        driver   : instancia activa de WebDriver
        usuario  : nombre de usuario (por defecto: standard_user)
        password : contraseña (por defecto: secret_sauce)
    """
    driver.get(URL_BASE)
 
    # Localizamos los campos por su atributo 'id' (localizador más robusto)
    campo_usuario   = driver.find_element(By.ID, "user-name")
    campo_password  = driver.find_element(By.ID, "password")
    boton_login     = driver.find_element(By.ID, "login-button")
 
    campo_usuario.clear()
    campo_usuario.send_keys(usuario)
 
    campo_password.clear()
    campo_password.send_keys(password)
 
    boton_login.click()
 
 
def esperar_redireccion_inventario(driver, timeout=TIMEOUT):
    """
    Espera explícita hasta que la URL contenga '/inventory.html'.
 
    Retorna True si la redirección ocurre antes del timeout,
    lanza TimeoutException si no ocurre.
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.url_contains("/inventory.html")
        )
        return True
    except TimeoutException:
        raise TimeoutException(
            f"La URL no cambió a /inventory.html en {timeout} segundos. "
            f"URL actual: {driver.current_url}"
        )
 
 
# ============================================================
#  Funciones de Inventario
# ============================================================
 
def obtener_titulos_productos(driver):
    """
    Devuelve una lista con los nombres de todos los productos visibles.
 
    Retorna:
        list[str]: nombres de productos en la página de inventario
    """
    elementos = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    return [elem.text for elem in elementos]
 
 
def obtener_precios_productos(driver):
    """
    Devuelve una lista con los precios de todos los productos visibles.
 
    Retorna:
        list[str]: precios como strings (ej. '$29.99')
    """
    elementos = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    return [elem.text for elem in elementos]
 
 
def verificar_elemento_presente(driver, by, selector, timeout=TIMEOUT):
    """
    Verifica con espera explícita que un elemento esté visible en pantalla.
 
    Args:
        by       : estrategia de localización (By.ID, By.CLASS_NAME, etc.)
        selector : valor del localizador
        timeout  : segundos máximos de espera
 
    Retorna:
        WebElement si se encuentra, lanza TimeoutException si no.
    """
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, selector))
    )
 
 
# ============================================================
#  Funciones de Carrito
# ============================================================
 
def agregar_primer_producto_al_carrito(driver):
    """
    Hace clic en el botón 'Add to cart' del primer producto de la lista.
 
    Retorna:
        str: nombre del producto agregado (para validar luego en el carrito)
    """
    # Obtenemos el nombre antes de agregar (para verificación posterior)
    nombre_producto = driver.find_elements(
        By.CLASS_NAME, "inventory_item_name"
    )[0].text
 
    # Clic en el primer botón 'Add to cart'
    botones_agregar = driver.find_elements(
        By.CSS_SELECTOR, ".btn_inventory"
    )
    botones_agregar[0].click()
 
    return nombre_producto
 
 
def obtener_contador_carrito(driver):
    """
    Lee el número que muestra el ícono del carrito en el encabezado.
 
    Retorna:
        int  : cantidad de ítems en el carrito
        None : si el contador no está visible (carrito vacío)
    """
    try:
        badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        return int(badge.text)
    except Exception:
        return None  # El badge no aparece si el carrito está vacío
 
 
def navegar_al_carrito(driver):
    """Hace clic en el ícono del carrito para ir a la página del carrito."""
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
 
 
def obtener_productos_en_carrito(driver):
    """
    Devuelve los nombres de los productos que aparecen en el carrito.
 
    Retorna:
        list[str]: nombres de ítems dentro del carrito
    """
    items = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    return [item.text for item in items]
 
 
# ============================================================
#  Funciones de Evidencia (capturas de pantalla)
# ============================================================
 
def tomar_captura_en_fallo(driver, nombre_test):
    """
    Guarda una captura de pantalla en la carpeta reports/screenshots/.
    Se llama automáticamente cuando un test falla.
 
    Args:
        driver      : instancia activa de WebDriver
        nombre_test : nombre del test para identificar el archivo
    """
    carpeta = os.path.join("reports", "screenshots")
    os.makedirs(carpeta, exist_ok=True)
 
    # Timestamp en el nombre para evitar sobreescrituras
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    ruta = os.path.join(carpeta, f"{nombre_test}_{timestamp}.png")
 
    driver.save_screenshot(ruta)
    print(f"\n📸 Captura guardada: {ruta}")
    return ruta
 