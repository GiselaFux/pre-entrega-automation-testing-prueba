# ============================================================
#  conftest.py — Configuracion global de pytest
#
#  Este archivo es detectado automaticamente por pytest.
#  Define el fixture "driver" que levanta y cierra Chrome
#  antes y despues de cada test, garantizando aislamiento.
#
#  Selenium 4 incluye su propio gestor de drivers: detecta
#  la version de Chrome instalada y descarga el ChromeDriver
#  correcto automaticamente, sin librerias externas.
# ============================================================

import pytest
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function")
def driver():
    """
    Fixture que provee un WebDriver de Chrome para cada test.

    scope="function" significa que se crea un navegador nuevo
    por cada funcion de test, garantizando independencia total
    entre pruebas (la falla de una no afecta a las demas).

    Selenium 4 gestiona el ChromeDriver automaticamente:
    no es necesario instalar ni configurar nada extra.
    """

    # --- Configuracion de opciones de Chrome ---
    chrome_options = Options()
    # Descomentar la siguiente linea para modo sin ventana (CI/CD):
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # --- Inicio del WebDriver ---
    # Selenium 4 detecta Chrome y descarga el driver correcto solo-no necesita Service()
    driver = webdriver.Chrome(options=chrome_options)

    # Espera implicita global: maximo 10s buscando cualquier elemento
    driver.implicitly_wait(10)

    # --- Entrega el driver al test ---
    yield driver

    # --- Teardown: cierra el navegador al finalizar el test ---
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook que captura una screenshot automaticamente si un test falla.
    La imagen se guarda en reports/screenshots/ con nombre y timestamp.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            carpeta = os.path.join("reports", "screenshots")
            os.makedirs(carpeta, exist_ok=True)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            nombre = item.name.replace(" ", "_")
            ruta = os.path.join(carpeta, f"FALLO_{nombre}_{timestamp}.png")
            driver.save_screenshot(ruta)
            print(f"\n Screenshot guardada: {ruta}")