import json

from app.models import Producto, DEFAULT_PRODUCTS


def test_carrito_total_vacio(client):
    response = client.get('/api/carrito/total')
    assert response.status_code == 200
    assert response.get_json()['total'] == 0


def test_agregar_carrito_con_cantidad_default(client):
    response = client.post(
        '/api/carrito',
        data=json.dumps({'producto_id': 2}),
        content_type='application/json'
    )
    assert response.status_code == 201

    response = client.get('/api/carrito')
    assert response.status_code == 200
    carrito = response.get_json()
    assert carrito[0]['cantidad'] == 1
    assert carrito[0]['producto']['id'] == 2
