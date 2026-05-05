// Configuración - CAMBIA ESTA URL POR TU SERVIDOR FLASK
const API_URL = 'http://localhost:5000/api'; // Cambia esto por tu URL real cuando esté en producción

// Elementos del DOM
const productosContainer = document.getElementById('productos-container');
const carritoContainer = document.getElementById('carrito-container');
const totalPrice = document.getElementById('total-price');
const btnCheckout = document.getElementById('btn-checkout');

// Estado de la aplicación
let productos = [];
let carrito = [];

// Cargar productos al iniciar
document.addEventListener('DOMContentLoaded', () => {
    cargarProductos();
    cargarCarrito();
});

// Cargar productos del API
async function cargarProductos() {
    try {
        const response = await fetch(`${API_URL}/productos`);
        if (!response.ok) throw new Error('Error al cargar productos');

        productos = await response.json();
        mostrarProductos();
    } catch (error) {
        console.error('Error:', error);
        productosContainer.innerHTML = '<p style="color: red;">Error al cargar los productos. Verifica que la API esté corriendo.</p>';
    }
}

// Mostrar productos en la página
function mostrarProductos() {
    productosContainer.innerHTML = '';

    productos.forEach(producto => {
        const card = document.createElement('div');
        card.className = 'producto-card';
        card.innerHTML = `
            <h3>${producto.nombre}</h3>
            <p>${producto.descripcion}</p>
            <div class="producto-info">
                <span class="producto-precio">$${producto.precio.toLocaleString('es-AR')}</span>
                <span class="producto-duracion">⏱️ ${producto.duracion_horas} hs</span>
            </div>
            <div class="producto-actions">
                <input type="number" class="cantidad-input" value="1" min="1" max="10" id="cant-${producto.id}">
                <button class="btn-agregar" onclick="agregarAlCarrito(${producto.id})">
                    Agregar
                </button>
            </div>
        `;
        productosContainer.appendChild(card);
    });
}

// Agregar producto al carrito
async function agregarAlCarrito(productoId) {
    const cantidadInput = document.getElementById(`cant-${productoId}`);
    const cantidad = parseInt(cantidadInput.value);

    if (cantidad <= 0) {
        alert('Ingresa una cantidad válida');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/carrito`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                producto_id: productoId,
                cantidad: cantidad
            })
        });

        if (!response.ok) throw new Error('Error al agregar al carrito');

        const data = await response.json();
        console.log(data.mensaje);

        // Resetear cantidad a 1
        cantidadInput.value = 1;

        // Recargar carrito
        cargarCarrito();
    } catch (error) {
        console.error('Error:', error);
        alert('Error al agregar el producto al carrito. Verifica la conexión con la API.');
    }
}

// Cargar carrito del API
async function cargarCarrito() {
    try {
        const response = await fetch(`${API_URL}/carrito`);
        if (!response.ok) throw new Error('Error al cargar carrito');

        carrito = await response.json();
        mostrarCarrito();
        actualizarTotal();
    } catch (error) {
        console.error('Error:', error);
        carritoContainer.innerHTML = '<p style="color: red;">Error al cargar el carrito. Verifica la conexión con la API.</p>';
    }
}

// Mostrar carrito en la página
function mostrarCarrito() {
    carritoContainer.innerHTML = '';

    if (carrito.length === 0) {
        carritoContainer.innerHTML = '<p class="empty-cart">El carrito está vacío</p>';
        btnCheckout.disabled = true;
        return;
    }

    btnCheckout.disabled = false;

    carrito.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'carrito-item';
        itemDiv.innerHTML = `
            <div class="carrito-item-info">
                <h4>${item.producto.nombre}</h4>
                <p>$${item.producto.precio.toLocaleString('es-AR')} c/u</p>
            </div>
            <div class="carrito-item-cantidad">
                <span>Cantidad</span>
                <strong>${item.cantidad}</strong>
            </div>
            <div style="text-align: right; flex: 0 0 100px;">
                <div style="font-weight: bold; color: #667eea; margin-bottom: 10px;">
                    $${(item.producto.precio * item.cantidad).toLocaleString('es-AR')}
                </div>
                <button class="btn-eliminar" onclick="eliminarDelCarrito(${item.producto.id})">
                    Eliminar
                </button>
            </div>
        `;
        carritoContainer.appendChild(itemDiv);
    });
}

// Eliminar producto del carrito
async function eliminarDelCarrito(productoId) {
    if (!confirm('¿Deseas eliminar este producto del carrito?')) return;

    try {
        const response = await fetch(`${API_URL}/carrito/${productoId}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Error al eliminar del carrito');

        const data = await response.json();
        console.log(data.mensaje);

        // Recargar carrito
        cargarCarrito();
    } catch (error) {
        console.error('Error:', error);
        alert('Error al eliminar el producto. Verifica la conexión con la API.');
    }
}

// Actualizar total
async function actualizarTotal() {
    try {
        const response = await fetch(`${API_URL}/carrito/total`);
        if (!response.ok) throw new Error('Error al obtener total');

        const data = await response.json();
        totalPrice.textContent = '$' + data.total.toLocaleString('es-AR');
    } catch (error) {
        console.error('Error:', error);
        totalPrice.textContent = '$0';
    }
}

// Proceder a compra
btnCheckout.addEventListener('click', () => {
    if (carrito.length === 0) {
        alert('El carrito está vacío');
        return;
    }

    alert('¡Gracias por tu compra!\n\nTotal: ' + totalPrice.textContent + '\n\nEsta es una demostración. En producción, procederías al pago.');

    // Aquí iría la integración con pasarela de pago
    console.log('Procesando compra...');
    console.log('Carrito:', carrito);
});