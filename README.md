#  Automatización de Testing — SauceDemo

Suite de pruebas automatizadas para el sitio [saucedemo.com](https://www.saucedemo.com) desarrollada como proyecto de pre-entrega del curso de QA Automation.



##  Propósito del Proyecto

Automatizar flujos críticos de navegación en SauceDemo utilizando **Selenium WebDriver** y **pytest**, aplicando buenas prácticas de QA como:

- Separación entre lógica de tests y funciones auxiliares
- Esperas explícitas para evitar tests frágiles
- Tests independientes entre sí
- Capturas de pantalla automáticas ante fallos
- Reporte HTML con resultados de ejecución



## Tecnologías Utilizadas

| Tecnología | Versión | Rol |

| Python | 3.10+ | Lenguaje principal |
| Selenium WebDriver | 4.18.1 | Automatización del navegador (incluye ChromeDriver Manager) |
| pytest | 8.1.1 | Framework de testing |
| pytest-html | 4.1.1 | Generación de reportes HTML |
| Git + GitHub | — | Control de versiones |

##  Estructura del Proyecto


pre-entrega-automation-testing-fuxgisela/
│
├── tests/
│   └── test_saucedemo.py    # Casos de prueba (login, catálogo, carrito)
│   └── conftest.py          # Setup/teardown global del WebDriver
├── utils/
│   ├── __init__.py          # Convierte utils/ en paquete Python
│   └── helpers.py           # Funciones reutilizables
│
├── reports/
│   ├── reporte.html         # Reporte generado por pytest-html
│   └── screenshots/         # Capturas automáticas en caso de fallo
│

├── requirements.txt         # Dependencias del proyecto
├── .gitignore               # Archivos excluidos del repositorio
└── README.md                # Este archivo



## Instalación de Dependencias

### Requisitos previos

- Python 3.10 o superior instalado
- Google Chrome instalado
- Git instalado

### Pasos

#  He Crear en Github el repositorio remoto, donde envie el proyecto

#  He Crear entorno virtual
python -m venv venv

# En Windows:
venv\Scripts\activate


#  Instalar dependencias
pip install -r requirements.txt



## Cómo Ejecutar las Pruebas

### Ejecutar todos los tests con reporte HTML


pytest tests/test_saucedemo.py -v --html=reports/reporte.html


### Ejecutar un test específico


# Solo el test de login
pytest tests/test_saucedemo.py::TestLogin::test_login_exitoso -v

# Solo los tests del carrito
pytest tests/test_saucedemo.py::TestCarrito -v



###  Casos de Prueba

| # | Clase | Test | Descripción |

| 1 | `TestLogin` | `test_login_exitoso` | Login con credenciales válidas → valida URL e inventario |
| 2 | `TestLogin` | `test_login_con_usuario_invalido` | Login inválido → verifica mensaje de error |
| 3 | `TestCatalogo` | `test_catalogo_inventario` | Valida título, productos, menú y filtros |
| 4 | `TestCarrito` | `test_agregar_producto_al_carrito` | Agrega producto, verifica badge y contenido del carrito |
| 5 | `TestCarrito` | `test_boton_cambia_a_remove_tras_agregar` | Verifica cambio de estado del botón |

### Credenciales de prueba (provistas por SauceDemo)


Usuario  : standard_user
Password : secret_sauce


##  Reporte HTML

Tras ejecutar las pruebas, el reporte se genera en `reports/reporte.html`.

Abrirlo en el navegador:
# Windows
start reports/reporte.html

##  Capturas de Pantalla

En caso de fallo, se guardan automáticamente en `reports/screenshots/` con el nombre del test y timestamp.

##  Autor

Gisela Fux 
Curso de QA Automation 
GitHub:https://github.com/GiselaFux
 