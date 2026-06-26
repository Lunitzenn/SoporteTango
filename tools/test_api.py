import json
import time
from urllib.request import urlopen, Request

base = 'http://127.0.0.1:5000'

def get(path):
    url = base + path
    req = Request(url, headers={'User-Agent': 'test-client'})
    with urlopen(req, timeout=5) as resp:
        return resp.read().decode('utf-8')

if __name__ == '__main__':
    # Esperar un momento para que el servidor arranque
    time.sleep(1)
    try:
        print('GET /api/productos')
        prod = get('/api/productos')
        print(prod)
    except Exception as e:
        print('Error al pedir /api/productos:', e)

    try:
        print('\nGET /api/carrito')
        cart = get('/api/carrito')
        print(cart)
    except Exception as e:
        print('Error al pedir /api/carrito:', e)
