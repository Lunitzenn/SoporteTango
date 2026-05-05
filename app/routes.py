from flask import Blueprint, jsonify, request
from flask_restx import Api, Resource, fields
from app.models import Producto, Carrito

# Datos iniciales de cursos de Tango Gestión
productos_db = [
    Producto(1, "Tango Básico", "Nivel inicial de Tango Gestión.Vista general de modulos. Asincronico.", 55000, 10),
    Producto(2, "Tango Intermedio", "Para profundizar en las técnicas, parametros y casos de uso. 10hs Asincronico 5hs Sincronico.", 552000, 15),
    Producto(3, "Sueldos y Control de Personal", "Administración de capital humano.10hs Asincronico 5hs Sincronico.", 638000, 15),
    Producto(4, "Sueldos Básico", "Tango Sueldos nivel básico, solo liquidación y control. Asincronico.", 199000, 10),
]

carrito = Carrito()

# Blueprint + API
api_bp = Blueprint('api', __name__)
api = Api(api_bp, 
          version='1.0', 
          title='TangoNat Cursos API',
          description='API REST para carrito de cursos de Tango')

# Modelos para Swagger
producto_model = api.model('Producto', {
    'id': fields.Integer,
    'nombre': fields.String,
    'descripcion': fields.String,
    'precio': fields.Float,
    'duracion_horas': fields.Integer
})

item_carrito_model = api.model('ItemCarrito', {
    'producto': fields.Nested(producto_model),
    'cantidad': fields.Integer
})

# ==================== ENDPOINTS ====================

@api.route('/productos')
class ListaProductos(Resource):
    @api.marshal_list_with(producto_model)
    def get(self):
        """Listar todos los cursos disponibles"""
        return productos_db


@api.route('/carrito')
class CarritoResource(Resource):
    @api.marshal_list_with(item_carrito_model)
    def get(self):
        """Obtener el contenido actual del carrito"""
        return carrito.items

    def post(self):
        """Agregar un producto al carrito"""
        data = request.get_json()
        producto_id = data.get('producto_id')
        cantidad = data.get('cantidad', 1)

        producto = next((p for p in productos_db if p.id == producto_id), None)
        if not producto:
            return {"error": "Producto no encontrado"}, 404

        carrito.agregar(producto, cantidad)
        return {"mensaje": f"Agregado {cantidad} x {producto.nombre} al carrito"}, 201


@api.route('/carrito/total')
class TotalCarrito(Resource):
    def get(self):
        """Calcular el total de la compra"""
        return {"total": carrito.total()}


@api.route('/carrito/<int:producto_id>')
class EliminarDelCarrito(Resource):
    def delete(self, producto_id):
        """Eliminar un producto del carrito"""
        carrito.eliminar(producto_id)
        return {"mensaje": "Producto eliminado del carrito"}, 200