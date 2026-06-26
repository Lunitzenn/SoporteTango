"""
API REST con Flask-RESTX
=========================
Endpoints para el carrito de compras.

Tecnologías:
- Flask-RESTX: crea API REST con documentación Swagger automática
- SQLAlchemy ORM: interactúa con PostgreSQL
- Sessions: identifica a cada usuario sin necesidad de login

Estructura:
- GET /api/productos: listar productos
- GET /api/carrito: obtener items del carrito
- POST /api/carrito: agregar producto al carrito
- DELETE /api/carrito/<id>: eliminar un producto
- DELETE /api/carrito/vaciar/todo: vaciar carrito completo
- GET /api/carrito/total: obtener total de la compra

Acceso a documentación: http://localhost:5000/api/doc
"""

from flask import Blueprint, jsonify, request, session
from flask_restx import Api, Resource, fields
from app.models import Producto, Cart, CartItem, db


# ============================================================
# GESTIÓN DE SESIONES Y CARRITOS
# ============================================================
def get_session_cart_id():
    """
    Obtiene o crea el ID del carrito del usuario actual.
    
    Usa las sesiones de Flask (cookies) para identificar a cada usuario.
    
    Lógica:
    1. ¿Existe cart_id en la sesión? Si sí, devolverlo
    2. Si no, crear un nuevo Cart en BD
    3. Guardar el cart_id en la sesión (cookie)
    4. Devolver el cart_id
    
    Ventajas:
    - Cada usuario tiene su propio carrito
    - Persiste entre visitas (mientras no expire la sesión)
    - No requiere autenticación
    
    Returns:
        int: ID del carrito del usuario actual
    """
    # Obtener cart_id de la sesión (cookie del navegador)
    cart_id = session.get('cart_id')
    
    if cart_id:
        # Si ya existe, devolverlo
        return cart_id
    
    # Si no existe, crear uno nuevo
    # Crear nueva instancia de Cart en la base de datos
    cart = Cart()
    db.session.add(cart)
    db.session.commit()  # Guardar en BD y obtener el ID asignado
    
    # Guardar el ID en la sesión del usuario
    # Esto se guarda automáticamente en una cookie del navegador
    session['cart_id'] = cart.id
    
    return cart.id


# ============================================================
# CONFIGURACIÓN DE API REST Y SWAGGER
# ============================================================
# Blueprint: agrupar rutas relacionadas
api_bp = Blueprint('api', __name__)

# Api: crear API REST con documentación Swagger automática
# La documentación estará disponible en http://localhost:5000/api/doc
api = Api(api_bp, 
          version='1.0',  # Versión de la API
          title='TangoNat Cursos API',  # Título en Swagger
          description='API REST para carrito de cursos de Tango')  # Descripción

# ============================================================
# DEFINIR MODELOS DE DATOS PARA SWAGGER
# ============================================================
# Estos modelos definen la estructura de datos que envía/recibe la API
# Se muestran automáticamente en la documentación Swagger

# Modelo: estructura de un Producto
producto_model = api.model('Producto', {
    'id': fields.Integer,
    'nombre': fields.String,
    'descripcion': fields.String,
    'precio': fields.Float,
    'duracion_horas': fields.Integer
})

# Modelo: estructura de un item del carrito
# Incluye un Producto anidado y la cantidad
item_carrito_model = api.model('ItemCarrito', {
    'producto': fields.Nested(producto_model),
    'cantidad': fields.Integer
})


# ============================================================
# ENDPOINTS - RECURSO: PRODUCTOS
# ============================================================
@api.route('/productos')
class ListaProductos(Resource):
    """
    Endpoint para listar todos los cursos disponibles.
    
    HTTP Method: GET
    URL: /api/productos
    """
    
    @api.marshal_list_with(producto_model)
    def get(self):
        """
        Listar todos los productos disponibles.
        
        Response: Lista de productos en JSON
        Status: 200 OK
        """
        # Consultar todos los productos de la tabla 'productos'
        productos = Producto.query.all()
        
        # Convertir a diccionarios JSON y devolver
        return [producto.to_dict() for producto in productos]


# ============================================================
# ENDPOINTS - RECURSO: CARRITO
# ============================================================
@api.route('/carrito')
class CarritoResource(Resource):
    """
    Endpoint para GET (ver carrito) y POST (agregar producto).
    
    HTTP Methods: GET, POST
    URL: /api/carrito
    """
    
    @api.marshal_list_with(item_carrito_model)
    def get(self):
        """
        Obtener todos los items del carrito del usuario actual.
        
        Response: Lista de items con producto y cantidad
        Status: 200 OK
        """
        # Obtener ID del carrito del usuario actual
        cart_id = get_session_cart_id()
        
        # Consultar todos los items que pertenecen a este carrito
        items = CartItem.query.filter_by(cart_id=cart_id).all()
        
        # Convertir a diccionarios y devolver
        return [item.to_dict() for item in items]

    def post(self):
        """
        Agregar un producto al carrito del usuario actual.
        
        Request Body (JSON):
            {
                "producto_id": 1,
                "cantidad": 2
            }
        
        Response: Mensaje de confirmación
        Status: 201 CREATED o 404 NOT FOUND
        """
        # Obtener datos JSON del cuerpo de la solicitud
        data = request.get_json()
        producto_id = data.get('producto_id')
        cantidad = data.get('cantidad', 1)  # Default 1 si no se especifica

        # Validar que el producto existe en la BD
        producto = Producto.query.get(producto_id)
        if not producto:
            # Devolver error 404 si el producto no existe
            return {"error": "Producto no encontrado"}, 404

        # Obtener el ID del carrito del usuario
        cart_id = get_session_cart_id()
        
        # Verificar si el producto ya está en el carrito
        item = CartItem.query.filter_by(cart_id=cart_id, producto_id=producto_id).first()
        
        if item:
            # Si ya está, incrementar la cantidad
            item.cantidad += cantidad
        else:
            # Si no está, crear un nuevo item
            item = CartItem(cart_id=cart_id, producto_id=producto_id, cantidad=cantidad)
            db.session.add(item)
        
        # Guardar cambios en la BD
        db.session.commit()
        
        # Devolver mensaje de éxito con status 201 (Created)
        return {"mensaje": f"Agregado {cantidad} x {producto.nombre} al carrito"}, 201


# ============================================================
# ENDPOINT - CALCULAR TOTAL
# ============================================================
@api.route('/carrito/total')
class TotalCarrito(Resource):
    """
    Endpoint para calcular el total del carrito.
    
    HTTP Method: GET
    URL: /api/carrito/total
    """
    
    def get(self):
        """
        Calcular el total de la compra.
        
        Fórmula: Σ(precio_producto × cantidad_producto) para cada item
        
        Response: {"total": 450000.0}
        Status: 200 OK
        """
        # Obtener ID del carrito del usuario
        cart_id = get_session_cart_id()
        
        # Obtener todos los items del carrito
        items = CartItem.query.filter_by(cart_id=cart_id).all()
        
        # Calcular total: suma de (precio × cantidad) para cada item
        # Si el carrito está vacío, devuelve 0
        total = sum(i.producto.precio * i.cantidad for i in items)
        
        return {"total": total}


# ============================================================
# ENDPOINT - ELIMINAR UN PRODUCTO DEL CARRITO
# ============================================================
@api.route('/carrito/<int:producto_id>')
class EliminarDelCarrito(Resource):
    """
    Endpoint para eliminar un producto específico del carrito.
    
    HTTP Method: DELETE
    URL: /api/carrito/<id>
    """
    
    def delete(self, producto_id):
        """
        Eliminar un producto del carrito.
        
        Args:
            producto_id (int): ID del producto a eliminar
        
        Response: Mensaje de confirmación
        Status: 200 OK
        """
        # Obtener ID del carrito del usuario
        cart_id = get_session_cart_id()
        
        # Eliminar el item que coincida con carrito y producto
        CartItem.query.filter_by(cart_id=cart_id, producto_id=producto_id).delete()
        
        # Guardar cambios en la BD
        db.session.commit()
        
        return {"mensaje": "Producto eliminado del carrito"}, 200


# ============================================================
# ENDPOINT - VACIAR TODO EL CARRITO
# ============================================================
@api.route('/carrito/vaciar/todo')
class VaciarCarrito(Resource):
    """
    Endpoint para vaciar completamente el carrito del usuario.
    
    HTTP Method: DELETE
    URL: /api/carrito/vaciar/todo
    
    Elimina TODOS los items de una sola vez.
    """
    
    def delete(self):
        """
        Vaciar todo el carrito (eliminar todos los items).
        
        Response: Mensaje de confirmación
        Status: 200 OK
        """
        # Obtener ID del carrito del usuario
        cart_id = get_session_cart_id()
        
        # Eliminar TODOS los items del carrito del usuario
        CartItem.query.filter_by(cart_id=cart_id).delete()
        
        # Guardar cambios en la BD
        db.session.commit()
        
        return {"mensaje": "Carrito vaciado correctamente"}, 200