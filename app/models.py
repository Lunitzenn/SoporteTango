"""
Modelos de Base de Datos (ORM)
===============================
Define los modelos SQLAlchemy que representan las tablas de la base de datos.

Estructuras:
- Producto: cursos disponibles
- Cart: carrito de cada usuario
- CartItem: items dentro del carrito (relación muchos-a-muchos)
"""

from flask_sqlalchemy import SQLAlchemy

# Inicializa SQLAlchemy para usar ORM (Object-Relational Mapping) con Flask
# El ORM permite trabajar con la BD usando objetos de Python en lugar de SQL directo
db = SQLAlchemy()

# ============================================================
# DATOS DE EJEMPLO
# ============================================================
# Estos productos se cargan automáticamente en la BD si está vacía
# Son cursos de Tango Gestión y Sueldos con precios en pesos argentinos
DEFAULT_PRODUCTS = [
    {
        'id': 1,
        'nombre': 'Tango Básico',
        'descripcion': 'Nivel inicial de Tango Gestión. Vista general de modulos. Asincronico.',
        'precio': 55000,
        'duracion_horas': 10,
    },
    {
        'id': 2,
        'nombre': 'Tango Intermedio',
        'descripcion': 'Para profundizar en las técnicas, parametros y casos de uso. 10hs Asincronico 5hs Sincronico.',
        'precio': 552000,
        'duracion_horas': 15,
    },
    {
        'id': 3,
        'nombre': 'Sueldos y Control de Personal',
        'descripcion': 'Administración de capital humano.10hs Asincronico 5hs Sincronico.',
        'precio': 638000,
        'duracion_horas': 15,
    },
    {
        'id': 4,
        'nombre': 'Sueldos Básico',
        'descripcion': 'Tango Sueldos nivel básico, solo liquidación y control. Asincronico.',
        'precio': 199000,
        'duracion_horas': 10,
    },
]


# ============================================================
# TABLA 1: PRODUCTOS
# ============================================================
class Producto(db.Model):
    """
    Modelo que representa un curso disponible en la tienda.
    
    Esta clase mapea a la tabla 'productos' en PostgreSQL.
    Cada producto es un curso de Tango que se puede agregar al carrito.
    
    Atributos:
        id: identificador único del producto (clave primaria)
        nombre: nombre del curso (ej: "Tango Básico")
        descripcion: descripción detallada del curso
        precio: precio en pesos argentinos
        duracion_horas: duración del curso en horas
    """
    __tablename__ = 'productos'

    # Clave primaria: identificador único para cada producto
    id = db.Column(db.Integer, primary_key=True)
    
    # Nombre del curso (máximo 128 caracteres, requerido)
    nombre = db.Column(db.String(128), nullable=False)
    
    # Descripción del curso (texto sin límite de caracteres, requerido)
    descripcion = db.Column(db.Text, nullable=False)
    
    # Precio del curso en pesos argentinos (requerido)
    precio = db.Column(db.Float, nullable=False)
    
    # Duración en horas de clase (requerido)
    duracion_horas = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        """
        Convierte el objeto Producto a un diccionario JSON.
        Utilizado para serializar datos cuando se envían como respuesta API.
        
        Returns:
            dict: diccionario con los datos del producto
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'duracion_horas': self.duracion_horas,
        }

    def __repr__(self):
        """Representación en texto del producto para debugging."""
        return f'<Producto {self.id} {self.nombre}>'


# ============================================================
# TABLA 2: CARRITOS
# ============================================================
class Cart(db.Model):
    """
    Modelo que representa el carrito de un usuario.
    
    Cada usuario/sesión tiene su propio carrito identificado por cart_id.
    El cart_id se guarda en la cookie de sesión del navegador.
    
    Esto permite:
    - Que cada usuario tenga su propio carrito
    - Persistencia entre visitas (mientras la cookie exista)
    - Sin necesidad de autenticación
    
    Relación: 1 Cart tiene MUCHOS CartItems
    """
    __tablename__ = 'carritos'

    # Clave primaria: identificador único del carrito
    id = db.Column(db.Integer, primary_key=True)


# ============================================================
# TABLA 3: ITEMS DEL CARRITO
# ============================================================
class CartItem(db.Model):
    """
    Modelo que representa un elemento dentro de un carrito.
    
    CartItem es la tabla de relación entre Cart y Producto.
    Cada CartItem representa "este producto está en este carrito con esta cantidad".
    
    Relaciones:
    - Muchos CartItems pertenecen a 1 Cart (many-to-one)
    - Muchos CartItems referencian 1 Producto (many-to-one)
    - Relación: Cart (1) ----< CartItem (N) >---- Producto (1)
    
    Atributos:
        id: identificador único del item
        cart_id: ID del carrito (clave foránea)
        producto_id: ID del producto (clave foránea)
        cantidad: cuántas unidades de este producto hay en el carrito
    """
    __tablename__ = 'cart_items'

    # Clave primaria: identificador único del item del carrito
    id = db.Column(db.Integer, primary_key=True)
    
    # Clave foránea: referencia a qué carrito pertenece este item
    # ON DELETE CASCADE: si se elimina el carrito, se eliminan sus items
    cart_id = db.Column(db.Integer, db.ForeignKey('carritos.id'), nullable=False)
    
    # Clave foránea: referencia a qué producto es este item
    # ON DELETE CASCADE: si se elimina un producto, se eliminan los items relacionados
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    
    # Cantidad de unidades de este producto en el carrito (por defecto 1)
    cantidad = db.Column(db.Integer, nullable=False, default=1)

    # Relación: permite acceder directamente al Producto desde el CartItem
    # lazy='joined': carga el producto automáticamente al obtener el CartItem
    # Uso: cartitem.producto.nombre (accede a nombre del producto)
    producto = db.relationship('Producto', lazy='joined')

    def to_dict(self):
        """
        Convierte el CartItem a formato JSON para la API.
        Incluye información completa del producto y la cantidad.
        
        Returns:
            dict: {'producto': {...}, 'cantidad': N}
        """
        return {
            'producto': self.producto.to_dict(),
            'cantidad': self.cantidad
        }


# ============================================================
# INICIALIZACIÓN DE LA BASE DE DATOS
# ============================================================
def init_db():
    """
    Inicializa la base de datos al arrancar la aplicación.
    
    Acciones:
    1. Crea todas las tablas (si no existen)
    2. Carga productos de ejemplo si la tabla 'productos' está vacía
    
    Se llama automáticamente en app/__init__.py
    """
    # Crear todas las tablas según los modelos definidos
    db.create_all()
    
    # Si no hay productos, cargar los de ejemplo
    # Esto ocurre solo la primera vez que se ejecuta la aplicación
    if Producto.query.count() == 0:
        for producto_data in DEFAULT_PRODUCTS:
            # Crear instancia del modelo Producto con los datos
            producto = Producto(**producto_data)
            # Agregar a la sesión (para guardar en BD)
            db.session.add(producto)
        # Confirmar los cambios en la BD (commit)
        db.session.commit()
