"""
Factory Pattern de Flask - Inicialización de la Aplicación
===========================================================
Implementa el patrón Factory para crear la aplicación Flask.

Ventajas:
- Permite crear múltiples instancias de la app con diferentes configuraciones
- Facilita testing con configuración de prueba
- Separa la creación de la app de su ejecución
"""

from flask import Flask, render_template
from flask_cors import CORS
from app.config import Config
from app.routes import api_bp
from app.models import db, init_db


def create_app(test_config=None):
    """
    Factory function que crea y configura la aplicación Flask.
    
    Esta función sigue el patrón Factory Pattern, que permite:
    1. Crear la app con diferentes configuraciones
    2. Facilitar testing
    3. Separar la lógica de creación
    
    Args:
        test_config (dict, optional): configuración especial para testing.
                                     Si se proporciona, sobrescribe Config.
    
    Returns:
        Flask: instancia de aplicación Flask completamente configurada
    """
    
    # ============================================================
    # 1. CREAR INSTANCIA DE FLASK
    # ============================================================
    # Flask(__name__) detecta automáticamente la carpeta 'app/templates'
    # y 'app/static' para servir HTML y archivos estáticos
    app = Flask(__name__)
    
    
    # ============================================================
    # 2. CARGAR CONFIGURACIÓN
    # ============================================================
    # Cargar configuración por defecto desde config.py
    # (BASE_URL, SECRET_KEY, DATABASE_URI, etc.)
    app.config.from_object(Config)

    # Si se proporciona test_config, sobrescribir la configuración anterior
    # Esto permite usar una BD de prueba sin afectar la producción
    if test_config is not None:
        app.config.from_mapping(test_config)

    
    # ============================================================
    # 3. INICIALIZAR EXTENSIONES
    # ============================================================
    # Conectar SQLAlchemy (base de datos) a la aplicación Flask
    db.init_app(app)
    
    # Habilitar CORS (Cross-Origin Resource Sharing)
    # Permite que el frontend en http://localhost:3000 acceda a la API en http://localhost:5000
    # (importante para desarrollo con servidores separados)
    CORS(app)

    
    # ============================================================
    # 4. REGISTRAR BLUEPRINTS (Módulos de la aplicación)
    # ============================================================
    # Registrar la API REST en el prefijo '/api'
    # Esto agrupa todos los endpoints de la API bajo /api/productos, /api/carrito, etc.
    # También genera automáticamente documentación Swagger en /api/doc
    app.register_blueprint(api_bp, url_prefix='/api')

    
    # ============================================================
    # 5. INICIALIZAR BASE DE DATOS
    # ============================================================
    # Ejecutar init_db() dentro del contexto de la aplicación
    # Necesario porque SQLAlchemy requiere acceso a app.config
    with app.app_context():
        init_db()  # Crea tablas y carga productos de ejemplo

    
    # ============================================================
    # 6. DEFINIR RUTAS HTML (Page Routes)
    # ============================================================
    # Ruta raíz: servir la página principal del carrito
    @app.route('/')
    def carrito():
        """
        Ruta: GET /
        Devuelve: HTML del carrito (Carrito.html)
        render_template: busca el archivo en app/templates/
        """
        return render_template('Carrito.html')

    # Ruta alternativa para acceder al carrito
    # Permite acceder tanto en / como en /carrito
    @app.route('/carrito')
    def carrito_page():
        """
        Ruta: GET /carrito
        Devuelve: Mismo HTML que la raíz (Carrito.html)
        """
        return render_template('Carrito.html')

    
    # ============================================================
    # 7. DEVOLVER APLICACIÓN CONFIGURADA
    # ============================================================
    return app

