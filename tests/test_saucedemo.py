# ============================================================
#  tests/test_saucedemo.py — Suite de tests de automatización
#
#  Sitio objetivo : https://www.saucedemo.com
#  Framework      : pytest + Selenium WebDriver
#  Autor          : Gisela Fux 
#
#  Contiene 3 casos de prueba obligatorios:
#    1. test_login_exitoso          → verifica redirección y título
#    2. test_catalogo_inventario    → valida productos y UI del catálogo
#    3. test_agregar_producto_carrito → flujo completo add-to-cart
#
#  Cada test es INDEPENDIENTE: usa su propio driver (fixture en
#  conftest.py con scope="function") y no depende del estado
#  dejado por otro test.
#
#  Ejecutar con:
#    pytest tests/test_saucedemo.py -v --html=reports/reporte.html
# ============================================================
 
import pytest
from selenium.webdriver.common.by import By
 
# Importamos todas las funciones auxiliares desde utils/helpers.py
from utils.helpers import (
    realizar_login,
    esperar_redireccion_inventario,
    obtener_titulos_productos,
    obtener_precios_productos,
    verificar_elemento_presente,
    agregar_primer_producto_al_carrito,
    obtener_contador_carrito,
    navegar_al_carrito,
    obtener_productos_en_carrito,
    tomar_captura_en_fallo,
    URL_INVENTARIO,
    URL_CARRITO,
    USUARIO_VALIDO,
    PASSWORD_VALIDO,
)
 
 
# ============================================================
#  TEST 1: Automatización de Login
# ============================================================
 
class TestLogin:
    """
    Valida el flujo de autenticación con credenciales válidas.
 
    Criterios mínimos del enunciado:
    - Espera explícita en la redirección a /inventory.html
    - Validación de URL y título de la página de destino
    """
 
    def test_login_exitoso(self, driver):
        """
        Ingresa con credenciales válidas y verifica que:
          a) La URL cambia a /inventory.html
          b) El título de la página contiene 'Products' o 'Swag Labs'
        """
        # PASO 1: Realizar el login con credenciales estándar
        realizar_login(driver, USUARIO_VALIDO, PASSWORD_VALIDO)
 
        # PASO 2: Espera explícita — máximo 10s para la redirección
        try:
            esperar_redireccion_inventario(driver)
        except Exception as e:
            tomar_captura_en_fallo(driver, "test_login_exitoso")
            raise AssertionError(f"Redirección fallida: {e}")
 
        # PASO 3: Validar URL final
        url_actual = driver.current_url
        assert "/inventory.html" in url_actual, (
            f"Se esperaba /inventory.html en la URL, pero se obtuvo: {url_actual}"
        )
 
        # PASO 4: Validar título de página (debe contener 'Products' o 'Swag Labs')
        titulo_pagina = driver.title
        assert any(palabra in titulo_pagina for palabra in ["Swag Labs", "Products"]), (
            f"Título inesperado: '{titulo_pagina}'"
        )
 
        # PASO 5: Verificar que el header con el título de productos esté visible
        header_productos = verificar_elemento_presente(
            driver, By.CLASS_NAME, "title"
        )
        assert header_productos.text == "Products", (
            f"Header de productos incorrecto: '{header_productos.text}'"
        )
 
        print(f"\n✅ Login exitoso → URL: {url_actual} | Título: {titulo_pagina}")
 
    def test_login_con_usuario_invalido(self, driver):
        """
        Verifica que un usuario inválido NO accede al inventario
        y que se muestra un mensaje de error.
 
        (Test extra para demostrar independencia entre casos)
        """
        realizar_login(driver, "usuario_falso", "clave_falsa")
 
        # Con credenciales inválidas debería aparecer mensaje de error
        mensaje_error = verificar_elemento_presente(
            driver, By.CSS_SELECTOR, "[data-test='error']"
        )
        assert mensaje_error.is_displayed(), "No se mostró mensaje de error"
        assert "/inventory.html" not in driver.current_url, (
            "Un usuario inválido no debería acceder al inventario"
        )
 
        print(f"\n✅ Error mostrado correctamente: '{mensaje_error.text}'")
 
 
# ============================================================
#  TEST 2: Navegación y Verificación del Catálogo
# ============================================================
 
class TestCatalogo:
    """
    Valida la página de inventario: título, productos y elementos de UI.
 
    Criterios mínimos del enunciado:
    - Valida título de la página de inventario
    - Valida presencia de al menos un producto
    - Lista nombre y precio del primer producto
    """
 
    def test_catalogo_inventario(self, driver):
        """
        Verifica que la página de inventario muestre:
          a) Título 'Products' en el encabezado
          b) Al menos un producto visible
          c) Nombre y precio del primer producto
          d) Menú hamburguesa y filtro de ordenamiento presentes
        """
        # PASO 1: Login previo (cada test empieza desde cero)
        realizar_login(driver)
        esperar_redireccion_inventario(driver)
 
        # PASO 2: Validar título del encabezado de la página
        titulo_header = verificar_elemento_presente(
            driver, By.CLASS_NAME, "title"
        )
        assert titulo_header.text == "Products", (
            f"Título incorrecto: '{titulo_header.text}'"
        )
 
        # PASO 3: Verificar que exista al menos un producto
        titulos_productos = obtener_titulos_productos(driver)
        assert len(titulos_productos) > 0, (
            "No se encontraron productos en el inventario"
        )
 
        # PASO 4: Listar nombre y precio del primer producto
        precios_productos = obtener_precios_productos(driver)
        primer_nombre = titulos_productos[0]
        primer_precio = precios_productos[0]
 
        print(f"\n📦 Primer producto: '{primer_nombre}' → Precio: {primer_precio}")
        print(f"   Total de productos en catálogo: {len(titulos_productos)}")
 
        # PASO 5: Validar que el nombre y precio no estén vacíos
        assert primer_nombre != "", "El nombre del primer producto está vacío"
        assert primer_precio != "", "El precio del primer producto está vacío"
        assert "$" in primer_precio, (
            f"El precio no tiene formato válido: '{primer_precio}'"
        )
 
        # PASO 6: Verificar elementos importantes de la interfaz
        # 6a. Menú hamburguesa (navegación lateral)
        menu_hamburguesa = verificar_elemento_presente(
            driver, By.ID, "react-burger-menu-btn"
        )
        assert menu_hamburguesa.is_displayed(), "El menú hamburguesa no está visible"
 
        # 6b. Filtro/selector de ordenamiento de productos
        filtro_orden = verificar_elemento_presente(
            driver, By.CLASS_NAME, "product_sort_container"
        )
        assert filtro_orden.is_displayed(), "El filtro de ordenamiento no está visible"
 
        # 6c. Ícono del carrito en el encabezado
        icono_carrito = verificar_elemento_presente(
            driver, By.CLASS_NAME, "shopping_cart_link"
        )
        assert icono_carrito.is_displayed(), "El ícono del carrito no está visible"
 
        print(f"\n✅ Catálogo validado: menú ✓ | filtros ✓ | carrito ✓")
        print(f"   Todos los productos: {titulos_productos}")
 
 
# ============================================================
#  TEST 3: Interacción con Productos — Carrito
# ============================================================
 
class TestCarrito:
    """
    Valida el flujo completo de agregar un producto al carrito.
 
    Criterios mínimos del enunciado:
    - Agrega el primer producto al carrito
    - Verifica que el contador del carrito se incremente a 1
    - Navega al carrito y verifica que el producto esté presente
    """
 
    def test_agregar_producto_al_carrito(self, driver):
        """
        Flujo completo de carrito:
          a) Login → Inventario
          b) Agrega el primer producto
          c) Verifica badge del carrito = 1
          d) Navega al carrito
          e) Confirma que el producto está en el carrito
        """
        # PASO 1: Login e ir al inventario
        realizar_login(driver)
        esperar_redireccion_inventario(driver)
 
        # PASO 2: Verificar que el contador esté vacío antes de agregar
        contador_inicial = obtener_contador_carrito(driver)
        assert contador_inicial is None, (
            f"El carrito debería estar vacío al inicio, pero tiene: {contador_inicial}"
        )
 
        # PASO 3: Agregar el primer producto al carrito
        nombre_producto_agregado = agregar_primer_producto_al_carrito(driver)
        print(f"\n🛒 Producto agregado: '{nombre_producto_agregado}'")
 
        # PASO 4: Verificar que el contador del carrito se incrementó a 1
        contador_post_agregar = obtener_contador_carrito(driver)
        assert contador_post_agregar == 1, (
            f"El contador del carrito debería ser 1, pero es: {contador_post_agregar}"
        )
        print(f"   Badge del carrito: {contador_post_agregar} ✓")
 
        # PASO 5: Navegar a la página del carrito
        navegar_al_carrito(driver)
 
        # PASO 6: Verificar que la URL sea la del carrito
        assert "/cart.html" in driver.current_url, (
            f"No se redirigió al carrito. URL actual: {driver.current_url}"
        )
 
        # PASO 7: Verificar que el producto aparezca en el carrito
        productos_en_carrito = obtener_productos_en_carrito(driver)
        assert len(productos_en_carrito) == 1, (
            f"Se esperaba 1 producto en el carrito, se encontraron: {len(productos_en_carrito)}"
        )
 
        # PASO 8: Verificar que el nombre coincida con el agregado
        assert nombre_producto_agregado in productos_en_carrito, (
            f"'{nombre_producto_agregado}' no encontrado en el carrito. "
            f"Productos actuales: {productos_en_carrito}"
        )
 
        print(f"   Producto confirmado en carrito: '{productos_en_carrito[0]}' ✓")
        print(f"\n✅ Flujo de carrito completo exitoso")
 
    def test_boton_cambia_a_remove_tras_agregar(self, driver):
        """
        Verifica que el botón 'Add to cart' cambie a 'Remove'
        después de agregar el producto.
 
        (Test extra de buena práctica QA)
        """
        realizar_login(driver)
        esperar_redireccion_inventario(driver)
 
        # Identificar el primer botón antes de hacer clic
        primer_boton = driver.find_elements(
            By.CSS_SELECTOR, ".btn_inventory"
        )[0]
        texto_antes = primer_boton.text
        assert "Add to cart" in texto_antes or "ADD TO CART" in texto_antes, (
            f"Texto inesperado antes de agregar: '{texto_antes}'"
        )
 
        # Hacer clic
        primer_boton.click()
 
        # Verificar que ahora dice 'Remove'
        primer_boton_actualizado = driver.find_elements(
            By.CSS_SELECTOR, ".btn_inventory"
        )[0]
        texto_despues = primer_boton_actualizado.text
        assert "Remove" in texto_despues or "REMOVE" in texto_despues, (
            f"El botón debería decir 'Remove' pero dice: '{texto_despues}'"
        )
 
        print(f"\n✅ Botón cambió: '{texto_antes}' → '{texto_despues}'")