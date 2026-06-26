/**
 * CARRITO DE COMPRAS - Script Frontend
 * =====================================
 * 
 * Archivo: carrito-script.js
 * 
 * Descripción:
 * Controla la interacción del usuario con el carrito de compras.
 * Se comunica con la API REST backend mediante fetch() para:
 * - Cargar productos
 * - Agregar/eliminar productos del carrito
 * - Calcular y mostrar totales
 * 
 * Tecnologías:
 * - Fetch API: comunicación con backend
 * - Async/Await: operaciones asincrónicas
 * - DOM Manipulation: insertar HTML dinámicamente
 * - Template Literals: strings con variables
 */

// ============================================================
// CONFIGURACIÓN INICIAL
// ============================================================

/**
 * URL base de la API REST.
 * 
 * Lógica:
 * - Si se accede como archivo local (file://): usa http://localhost:5000/api
 * - Si se accede desde servidor: usa el mismo servidor + /api
 * 
 * Ejemplo:
 * - Desarrollo local: http://localhost:5000/api
 * - Producción: https://miapp.com/api
 */
const API_URL = window.location.protocol === 'file:' 
    ? 'http://localhost:5000/api' 
    : `${window.location.origin}/api`;

// ============================================================
// REFERENCIAS A ELEMENTOS HTML (DOM)
// ============================================================

// Contenedor donde se muestran los productos disponibles
const productosContainer = document.getElementById('productos-container');

// Contenedor donde se muestran los items del carrito
const carritoContainer = document.getElementById('carrito-container');

// Elemento que muestra el total de la compra
const totalPrice = document.getElementById('total-price');

// Botón "Proceder a Compra"
const btnCheckout = document.getElementById('btn-checkout');

// ============================================================
// ESTADO DE LA APLICACIÓN
// ============================================================

// Array que almacena la lista de productos del servidor
let productos = [];

// Array que almacena los items actualmente en el carrito
let carrito = [];


// ============================================================
// EVENTO: CUANDO CARGA LA PÁGINA
// ============================================================

/**
 * Evento DOMContentLoaded: se ejecuta cuando HTML está completamente cargado
 * 
 * Acciones al cargar:
 * 1. Cargar productos del servidor
 * 2. Cargar items del carrito del usuario
 */
document.addEventListener('DOMContentLoaded', () => {
    cargarProductos();    // Traer productos de la API
    cargarCarrito();      // Traer carrito del usuario
});


// ============================================================
// FUNCIÓN: CARGAR PRODUCTOS
// ============================================================

/**
 * Obtiene la lista de cursos disponibles del servidor API.
 * 
 * Llamada: GET /api/productos
 * 
 * Flujo:
 * 1. Enviar request GET a /api/productos
 * 2. Convertir respuesta a JSON
 * 3. Guardar en variable global 'productos'
 * 4. Mostrar productos en la página
 * 5. Si hay error, mostrar mensaje en rojo
 * 
 * async/await: permite esperar a que termine la solicitud HTTP
 */
async function cargarProductos() {
    try {
        // Enviar GET a /api/productos
        const response = await fetch(`${API_URL}/productos`);
        
        // Verificar si la respuesta fue exitosa (status 200)
        if (!response.ok) throw new Error('Error al cargar productos');

        // Convertir respuesta a JSON
        productos = await response.json();
        
        // Mostrar los productos en la página
        mostrarProductos();
        
    } catch (error) {
        // Si hay error, mostrar en consola y en pantalla
        console.error('Error:', error);
        productosContainer.innerHTML = '<p style="color: red;">Error al cargar los productos. Verifica que la API esté corriendo.</p>';
    }
}


// ============================================================
// FUNCIÓN: MOSTRAR PRODUCTOS EN LA PÁGINA
// ============================================================

/**
 * Crea tarjetas HTML para cada producto y las inserta en el DOM.
 * 
 * Para cada producto genera:
 * - Nombre y descripción
 * - Precio (formateado en pesos argentinos)
 * - Duración en horas
 * - Input para seleccionar cantidad
 * - Botón "Agregar" al carrito
 */
function mostrarProductos() {
    // Limpiar contenedor (borrar lo que había antes)
    productosContainer.innerHTML = '';

    // Iterar sobre cada producto
    productos.forEach(producto => {
        // Crear un div para la tarjeta del producto
        const card = document.createElement('div');
        card.className = 'producto-card';
        
        // Usar template literal para insertar HTML con variables
        // toLocaleString('es-AR'): formatea números con separadores de miles
        card.innerHTML = `
            <h3>${producto.nombre}</h3>
            <p>${producto.descripcion}</p>
            <div class="producto-info">
                <span class="producto-precio">$${producto.precio.toLocaleString('es-AR')}</span>
                <span class="producto-duracion">⏱️ ${producto.duracion_horas} hs</span>
            </div>
            <div class="producto-actions">
                <!-- Input para seleccionar cantidad (entre 1 y 10) -->
                <input type="number" class="cantidad-input" value="1" min="1" max="10" id="cant-${producto.id}">
                <!-- Botón que llama a agregarAlCarrito() -->
                <button class="btn-agregar" onclick="agregarAlCarrito(${producto.id})">
                    Agregar
                </button>
            </div>
        `;
        
        // Insertar la tarjeta en el contenedor
        productosContainer.appendChild(card);
    });
}


// ============================================================
// FUNCIÓN: AGREGAR PRODUCTO AL CARRITO
// ============================================================

/**
 * Agrega un producto al carrito del usuario.
 * 
 * Llamada: POST /api/carrito
 * 
 * Parámetro:
 * - productoId: ID del producto a agregar
 * 
 * Flujo:
 * 1. Obtener cantidad del input HTML
 * 2. Validar que cantidad > 0
 * 3. Enviar POST a /api/carrito con producto_id y cantidad
 * 4. Si funciona, resetear input y recargar carrito
 * 5. Si falla, mostrar alert
 */
async function agregarAlCarrito(productoId) {
    // Obtener el input de cantidad específico de este producto
    const cantidadInput = document.getElementById(`cant-${productoId}`);
    
    // Convertir a número
    const cantidad = parseInt(cantidadInput.value);

    // Validar que sea cantidad válida
    if (cantidad <= 0) {
        alert('Ingresa una cantidad válida');
        return;
    }

    try {
        // Enviar POST a /api/carrito con el producto y cantidad
        const response = await fetch(`${API_URL}/carrito`, {
            method: 'POST',  // POST para crear/agregar
            headers: {
                'Content-Type': 'application/json'  // Indicar que enviamos JSON
            },
            // Convertir objeto a JSON string
            body: JSON.stringify({
                producto_id: productoId,
                cantidad: cantidad
            })
        });

        // Verificar si fue exitoso
        if (!response.ok) throw new Error('Error al agregar al carrito');

        // Obtener respuesta del servidor
        const data = await response.json();
        console.log(data.mensaje);  // "Agregado 2 x Tango Básico al carrito"

        // Resetear el input a 1 para el siguiente
        cantidadInput.value = 1;

        // Recargar el carrito para mostrar el nuevo item
        cargarCarrito();
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error al agregar el producto al carrito. Verifica la conexión con la API.');
    }
}


// ============================================================
// FUNCIÓN: CARGAR CARRITO
// ============================================================

/**
 * Obtiene los items del carrito del usuario desde el servidor.
 * 
 * Llamada: GET /api/carrito
 * 
 * Flujo:
 * 1. Enviar GET a /api/carrito
 * 2. Convertir respuesta a JSON
 * 3. Guardar en variable 'carrito'
 * 4. Mostrar items del carrito
 * 5. Actualizar total de la compra
 */
async function cargarCarrito() {
    try {
        // GET a /api/carrito para obtener los items
        const response = await fetch(`${API_URL}/carrito`);
        if (!response.ok) throw new Error('Error al cargar carrito');

        // Convertir a JSON: [{ producto: {...}, cantidad: 2 }, ...]
        carrito = await response.json();
        
        // Mostrar items en la página
        mostrarCarrito();
        
        // Recalcular total
        actualizarTotal();
        
    } catch (error) {
        console.error('Error:', error);
        carritoContainer.innerHTML = '<p style="color: red;">Error al cargar el carrito. Verifica la conexión con la API.</p>';
    }
}


// ============================================================
// FUNCIÓN: MOSTRAR CARRITO EN LA PÁGINA
// ============================================================

/**
 * Muestra los items del carrito en la página.
 * 
 * Si carrito está vacío:
 * - Mostrar mensaje "El carrito está vacío"
 * - Desactivar botón "Proceder a Compra"
 * 
 * Si hay items:
 * - Mostrar cada item con nombre, precio unitario, cantidad, subtotal
 * - Botón para eliminar cada item
 * - Habilitar botón "Proceder a Compra"
 */
function mostrarCarrito() {
    // Limpiar contenedor
    carritoContainer.innerHTML = '';

    // Verificar si carrito está vacío
    if (carrito.length === 0) {
        // Mostrar mensaje
        carritoContainer.innerHTML = '<p class="empty-cart">El carrito está vacío</p>';
        // Desactivar botón de compra (no hay nada que comprar)
        btnCheckout.disabled = true;
        return;
    }

    // Si hay items, habilitar botón
    btnCheckout.disabled = false;

    // Iterar sobre cada item del carrito
    carrito.forEach(item => {
        // Crear div para el item
        const itemDiv = document.createElement('div');
        itemDiv.className = 'carrito-item';
        
        // Calcular subtotal: precio × cantidad
        const subtotal = item.producto.precio * item.cantidad;
        
        itemDiv.innerHTML = `
            <!-- Información del producto -->
            <div class="carrito-item-info">
                <h4>${item.producto.nombre}</h4>
                <p>$${item.producto.precio.toLocaleString('es-AR')} c/u</p>
            </div>
            
            <!-- Cantidad -->
            <div class="carrito-item-cantidad">
                <span>Cantidad</span>
                <strong>${item.cantidad}</strong>
            </div>
            
            <!-- Subtotal y botón eliminar -->
            <div style="text-align: right; flex: 0 0 100px;">
                <!-- Subtotal (precio × cantidad) -->
                <div style="font-weight: bold; color: #667eea; margin-bottom: 10px;">
                    $${subtotal.toLocaleString('es-AR')}
                </div>
                <!-- Botón para eliminar este item -->
                <button class="btn-eliminar" onclick="eliminarDelCarrito(${item.producto.id})">
                    Eliminar
                </button>
            </div>
        `;
        
        // Insertar item en el contenedor
        carritoContainer.appendChild(itemDiv);
    });
}


// ============================================================
// FUNCIÓN: ELIMINAR PRODUCTO DEL CARRITO
// ============================================================

/**
 * Elimina un producto específico del carrito.
 * 
 * Llamada: DELETE /api/carrito/<id>
 * 
 * Parámetro:
 * - productoId: ID del producto a eliminar
 * 
 * Flujo:
 * 1. Pedir confirmación al usuario
 * 2. Si confirma, enviar DELETE a /api/carrito/<id>
 * 3. Recargar carrito
 * 4. Si falla, mostrar alert
 */
async function eliminarDelCarrito(productoId) {
    // Pedir confirmación antes de eliminar
    if (!confirm('¿Deseas eliminar este producto del carrito?')) return;

    try {
        // DELETE a /api/carrito/<id>
        const response = await fetch(`${API_URL}/carrito/${productoId}`, {
            method: 'DELETE'
        });

        // Verificar si fue exitoso
        if (!response.ok) throw new Error('Error al eliminar del carrito');

        // Obtener mensaje
        const data = await response.json();
        console.log(data.mensaje);

        // Recargar carrito para reflejar cambios
        cargarCarrito();
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error al eliminar el producto. Verifica la conexión con la API.');
    }
}


// ============================================================
// FUNCIÓN: ACTUALIZAR TOTAL
// ============================================================

/**
 * Obtiene el total de la compra del servidor y lo muestra.
 * 
 * Llamada: GET /api/carrito/total
 * 
 * El total se calcula en el backend: suma(precio × cantidad)
 */
async function actualizarTotal() {
    try {
        // GET a /api/carrito/total
        const response = await fetch(`${API_URL}/carrito/total`);
        if (!response.ok) throw new Error('Error al obtener total');

        // Obtener JSON: { "total": 450000.0 }
        const data = await response.json();
        
        // Mostrar en el HTML formateado
        totalPrice.textContent = '$' + data.total.toLocaleString('es-AR');
        
    } catch (error) {
        console.error('Error:', error);
        totalPrice.textContent = '$0';
    }
}


// ============================================================
// EVENTO: BOTÓN PROCEDER A COMPRA
// ============================================================

/**
 * Listener para el botón "Proceder a Compra".
 * 
 * Actualmente: muestra un mensaje de demostración
 * 
 * En producción:
 * - Integrar con pasarela de pago (Stripe, MercadoPago, etc.)
 * - Procesar la transacción
 * - Guardar pedido en BD
 * - Limpiar carrito
 */
btnCheckout.addEventListener('click', () => {
    // Verificar que hay items para comprar
    if (carrito.length === 0) {
        alert('El carrito está vacío');
        return;
    }

    // Mensaje de demostración
    alert('¡Gracias por tu compra!\n\nTotal: ' + totalPrice.textContent + '\n\nEsta es una demostración. En producción, procederías al pago.');

    // Log para debugging
    console.log('Procesando compra...');
    console.log('Carrito:', carrito);
    
    // AQUÍ IRÍA:
    // - Llamada a pasarela de pago
    // - Guardar en BD
    // - Limpiar carrito
});


// ============================================================
// FUNCIÓN: VACIAR TODO EL CARRITO
// ============================================================

/**
 * Vacía completamente el carrito del usuario.
 * 
 * Llamada: DELETE /api/carrito/vaciar/todo
 * 
 * Flujo:
 * 1. Pedir confirmación al usuario (porque es operación destructiva)
 * 2. Si confirma, enviar DELETE a /api/carrito/vaciar/todo
 * 3. Elimina TODOS los items de una vez
 * 4. Recargar carrito (quedará vacío)
 * 5. Si falla, mostrar alert
 */
async function vaciarCarrito() {
    // Pedir confirmación porque es una acción importante
    if (!confirm('¿Estás seguro de que deseas vaciar el carrito completamente?')) return;
    
    try {
        // DELETE a /api/carrito/vaciar/todo (elimina TODOS los items)
        const response = await fetch(`${API_URL}/carrito/vaciar/todo`, {
            method: 'DELETE'
        });
        
        // Verificar si fue exitoso
        if (!response.ok) throw new Error('Error al vaciar el carrito');
        
        // Obtener mensaje
        const data = await response.json();
        console.log(data.mensaje);  // "Carrito vaciado correctamente"
        
        // Recargar carrito (quedará vacío)
        cargarCarrito();
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error al vaciar el carrito');
    }
}