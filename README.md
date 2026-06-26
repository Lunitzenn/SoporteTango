# SoporteTango - Proyecto PWEB2

Sitio Github en vista web (sin carrito funcional por limitaciones de Github):
https://lunitzenn.github.io/SoporteTango/contact.html


Repositorio Github: https://github.com/Lunitzenn/SoporteTango


**Carrito de compras para cursos de Tango con backend RESTful, frontend estático y pruebas completas.**

Este proyecto implementa una aplicación que permite seleccionar cursos, agregarlos al carrito, eliminar productos y calcular el total de la compra utilizando una API RESTful en Flask y PostgreSQL para persistencia.

---

## Descripción del Proyecto

SoporteTango es una aplicación diseñada para gestionar cursos de Tango a través de un carrito de compras. El flujo principal incluye:

- Listar cursos disponibles
- Agregar cursos al carrito
- Eliminar cursos del carrito
- Calcular el total de la compra
- Mantener un carrito único por visitante usando cookie/sesión
- Almacenar la información en PostgreSQL
- Ejecutar pruebas unitarias con pytest
- Ejecutar pruebas E2E con Cypress

El proyecto no usa inicio de sesión; cada visitante tiene un carrito independiente asociado a su sesión.

---

## Tecnologías utilizadas

- Python 3.14
- Flask
- Flask-RESTX
- Flask-CORS
- Flask-SQLAlchemy
- python-dotenv
- psycopg2-binary
- PostgreSQL
- JavaScript Vanilla
- Bootstrap / CSS estático
- pytest para pruebas unitarias
- Cypress para pruebas E2E
- npm / Node.js para ejecutar Cypress

---------------------------------------------------------------------------------

## Estructura del Proyecto

```bash
SoporteTango-main/
├── app/
│   ├── __init__.py           # Fábrica de Flask y registro de blueprint
│   ├── config.py             # Configuración de PostgreSQL y Flask
│   ├── models.py             # Modelos Producto, Cart y CartItem
│   ├── routes.py             # Endpoints de la API REST
│   ├── static/               # Archivos JavaScript y CSS del carrito
│   │   ├── carrito-script.js
│   │   └── carrito-styles.css
│   └── templates/            # Plantilla del carrito
│       └── Carrito.html
├── cypress/                  # Pruebas E2E con Cypress
│   ├── e2e/
│   │   └── cart_flow.cy.js
│   └── support/
│       ├── commands.js
│       └── e2.js
├── tests/                    # Pruebas unitarias con pytest
│   ├── conftest.py
│   ├── test_api.py
│   └── test_routes.py
├── tools/                    # Scripts de prueba y utilidades
│   ├── test_api.py
│   └── test_cart_actions.py
├── package.json              # Configuración de Cypress y npm
├── cypress.config.js         # Configuración de Cypress
├── pytest.ini                # Configuración de pytest
├── requirements.txt          # Dependencias Python
├── .env                      # Variables de entorno para PostgreSQL
└── run.py                    # Punto de entrada de la aplicación
```

------------------------------------------------------------------------------

## Instalación y ejecución

1. Instalar dependencias Python:
   ```bash
   pip install -r requirements.txt
   ```
2. Configurar el archivo `.env` con los datos de PostgreSQL:
   - `POSTGRES_USER`
   - `POSTGRES_PASSWORD`
   - `POSTGRES_HOST`
   - `POSTGRES_PORT`
   - `POSTGRES_DB`
3. Ejecutar la aplicación:
   
   python run.py
   
4. Abrir en el navegador:
   
   http://localhost:5000/carrito


---

## Pruebas

### Unitarias

Ejecutar:
```bash
pytest
```

### E2E con Cypress

1. Instalar dependencias npm:
   ```bash
   npm install
   ```
2. Ejecutar Cypress en modo abierto:
   ```bash
   npm run cy:open
   ```
3. Ejecutar Cypress en modo headless:
   ```bash
   npm run cy:run
   ```

---

## Resumen del estado del proyecto

El proyecto está compuesto por un backend Flask que expone una API REST bajo `/api`, un frontend estático que consume dicha API y una base de datos PostgreSQL que persiste productos y carritos. El carrito se genera sin login y se conserva por visitante mediante sesión. Se agregaron pruebas unitarias y E2E para cubrir el flujo de compra completo.

---

## Enlaces importantes

- Repositorio GitHub: https://github.com/Lunitzenn/SoporteTango
