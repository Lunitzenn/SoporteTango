from flask import Flask, render_template
from flask_cors import CORS
from app.config import Config
from app.routes import api_bp, api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)  # Permitir frontend en otro puerto
    
    # Registrar blueprint con el namespace de Swagger
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Ruta para servir el carrito
    @app.route('/')
    def carrito():
        return render_template('Carrito.html')
    
    # Alias /carrito para acceso directo
    @app.route('/carrito')
    def carrito_page():
        return render_template('Carrito.html')
    
    return app

