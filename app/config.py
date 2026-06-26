"""
Configuración de la aplicación Flask
======================================
Define las variables de configuración para diferentes entornos
(desarrollo, testing, producción).

Todas las configuraciones se cargan desde variables de entorno (.env)
para mantener información sensible fuera del código.
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env (no guardado en GitHub)
load_dotenv()


def database_uri() -> str:
    """
    Construye la URI de conexión para PostgreSQL dinámicamente.
    
    La URI tiene el formato: postgresql+psycopg2://usuario:contraseña@host:puerto/basedatos
    
    Usa variables de entorno:
    - DB_TYPE: tipo de base de datos (postgres por defecto)
    - POSTGRES_USER: usuario de PostgreSQL
    - POSTGRES_PASSWORD: contraseña de PostgreSQL
    - POSTGRES_HOST: host/servidor (localhost por defecto)
    - POSTGRES_PORT: puerto (5432 por defecto)
    - POSTGRES_DB: nombre de la base de datos
    
    Returns:
        str: URI de conexión completa a la base de datos
        
    Raises:
        ValueError: si el DB_TYPE no es soportado
    """
    db_type = os.getenv('DB_TYPE', 'postgres').lower()

    if db_type in ('postgres', 'postgresql'):
        # Obtener credenciales desde variables de entorno
        user = os.getenv('POSTGRES_USER', 'postgres')
        password = os.getenv('POSTGRES_PASSWORD', '')
        host = os.getenv('POSTGRES_HOST', 'localhost')
        port = os.getenv('POSTGRES_PORT', '5432')
        database = os.getenv('POSTGRES_DB', 'tango_gestion')
        
        # Construir la URI con el formato requerido por SQLAlchemy
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

    raise ValueError(
        f"Unsupported DB_TYPE '{db_type}'. Use 'postgres' or 'postgresql'."
    )


class Config:
    """
    Clase con la configuración principal de Flask y SQLAlchemy.
    
    Atributos:
        SECRET_KEY: clave secreta para encriptar sesiones (importante en producción)
        DEBUG: habilita modo debug (no usar en producción)
        SQLALCHEMY_DATABASE_URI: conexión a PostgreSQL
        SQLALCHEMY_TRACK_MODIFICATIONS: desactiva advertencias innecesarias de SQLAlchemy
    """
    
    # Clave secreta para cifrar datos de sesión. Cambiar en producción
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-tango-gestion')
    
    # Modo debug: activa recarga automática y mejor manejo de errores
    # IMPORTANTE: Desactivar en producción por razones de seguridad
    DEBUG = os.getenv('DEBUG', 'True').lower() in ('1', 'true', 'yes')
    
    # URI de conexión a la base de datos PostgreSQL
    SQLALCHEMY_DATABASE_URI = database_uri()
    
    # Evita que SQLAlchemy emita advertencias innecesarias
    SQLALCHEMY_TRACK_MODIFICATIONS = False



    