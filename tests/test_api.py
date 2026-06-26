import json

from app.models import Producto, DEFAULT_PRODUCTS


def test_listar_productos(client):
    response = client.get('/api/productos')
    assert response.status_code == 200

    productos = response.get_json()
    assert isinstance(productos, list)
    assert len(productos) == len(DEFAULT_PRODUCTS)
    assert productos[0]['nombre'] == DEFAULT_PRODUCTS[0]['nombre']


def test_carrito_inicial_vacio(client):
    response = client.get('/api/carrito')
    assert response.status_code == 200
    assert response.get_json() == []


def test_agregar_y_eliminar_producto_del_carrito(client):
    response = client.post(
        '/api/carrito',
        data=json.dumps({'producto_id': 1, 'cantidad': 2}),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = response.get_json()
    assert 'Agregado' in data['mensaje']

    response = client.get('/api/carrito')
    assert response.status_code == 200
    carrito = response.get_json()
    assert len(carrito) == 1
    assert carrito[0]['cantidad'] == 2
    assert carrito[0]['producto']['id'] == 1

    response = client.get('/api/carrito/total')
    assert response.status_code == 200
    total = response.get_json()['total']
    assert total == carrito[0]['producto']['precio'] * 2

    response = client.delete('/api/carrito/1')
    assert response.status_code == 200

    response = client.get('/api/carrito')
    assert response.status_code == 200
    assert response.get_json() == []
