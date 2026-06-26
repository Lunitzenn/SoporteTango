import json
import time
from urllib.request import Request, build_opener, HTTPCookieProcessor
from http.cookiejar import CookieJar

base = 'http://127.0.0.1:5000'


cookie_jar = CookieJar()
opener = build_opener(HTTPCookieProcessor(cookie_jar))


def request_json(method, path, data=None):
    url = base + path
    body = None
    headers = {'User-Agent': 'test-client'}
    if data is not None:
        body = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    req = Request(url, data=body, headers=headers, method=method)
    with opener.open(req, timeout=5) as resp:
        return resp.read().decode('utf-8')


if __name__ == '__main__':
    time.sleep(1)
    try:
        print('POST /api/carrito add producto 1 x2')
        resp = request_json('POST', '/api/carrito', {'producto_id': 1, 'cantidad': 2})
        print(resp)
    except Exception as e:
        print('Error POST:', e)

    try:
        print('\nGET /api/carrito')
        resp = request_json('GET', '/api/carrito')
        print(resp)
    except Exception as e:
        print('Error GET cart:', e)

    try:
        print('\nGET /api/carrito/total')
        resp = request_json('GET', '/api/carrito/total')
        print(resp)
    except Exception as e:
        print('Error GET total:', e)

    try:
        print('\nDELETE /api/carrito/1')
        resp = request_json('DELETE', '/api/carrito/1')
        print(resp)
    except Exception as e:
        print('Error DELETE:', e)

    try:
        print('\nGET /api/carrito (after delete)')
        resp = request_json('GET', '/api/carrito')
        print(resp)
    except Exception as e:
        print('Error GET cart after delete:', e)
