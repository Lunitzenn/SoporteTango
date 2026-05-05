# Tango Gestión API - Backend con Flask

**Etapa 1: Backend con APIs RESTful**  
**Programación Web 2 - UNO**
**Maria Natalia Mascarini**


API RESTful desarrollada con **Flask** para gestionar un carrito de compras de cursos de tango.

---

## 📋 Descripción del Proyecto

Esta API permite gestionar un carrito de compras de cursos de tango ofrecidos por nuestra empresa.  
Cumple con todos los requisitos mínimos solicitados:

- Listado de productos (cursos)
- Agregar productos al carrito
- Eliminar productos del carrito
- Calcular el total de la compra
- Persistencia inicial en memoria (sin base de datos)
- Documentación automática con **Swagger / OpenAPI**
- Preparado para CORS (futuro frontend)

---

## 🚀 Tecnologías Utilizadas

- **Python 3.10+**
- **Flask** (microframework)
- **Flask-RESTX** (para rutas REST y documentación Swagger)
- **Flask-CORS**
- **python-dotenv**
- Persistencia en memoria con estructuras de datos Python

---

## 📁 Estructura del Proyecto

```bash
tango-gestion-api/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py          # Modelos de Producto y Carrito
│   └── routes.py          # Endpoints REST + Swagger
├── tests/
│   └── test_api.py        # Tests unitarios (pendiente)
├── run.py                 # Archivo principal para ejecutar
├── requirements.txt
├── .env
├── README.md
└── venv/                  # Entorno virtual (esto no esta subido!)

## Muchas gracias por leer hasta aca!

###                                     Maria Natalia Mascarini

