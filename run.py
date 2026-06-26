"""
TangoNat - Carrito de Cursos de Tango
========================================
Archivo principal para ejecutar la aplicación Flask.
Este archivo inicia el servidor web que sirve la aplicación.

Autor: Maria Natalia Mascarini
Materia: PWEB2 (Programación Web II)
Fecha: Junio 2026
"""

from app import create_app

# Crear la aplicación Flask usando la fábrica de aplicaciones (patrón de diseño Factory Pattern)
# Esto permite crear la app con diferentes configuraciones (desarrollo, testing, producción)
app = create_app()

# Bloque principal: se ejecuta solo si este archivo se corre directamente
if __name__ == '__main__':
    # Ejecutar el servidor local en el puerto 5000
    # debug=True: reinicia el servidor cuando hay cambios en los archivos
    # port=5000: servidor disponible en http://localhost:5000
    app.run(debug=True, port=5000)
