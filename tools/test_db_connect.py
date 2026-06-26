import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Cargar variables de entorno del archivo .env
load_dotenv()

# Construir URI de PostgreSQL
user = os.getenv('POSTGRES_USER', 'postgres')
password = os.getenv('POSTGRES_PASSWORD', '')
host = os.getenv('POSTGRES_HOST', 'localhost')
port = os.getenv('POSTGRES_PORT', '5432')
database = os.getenv('POSTGRES_DB', 'tango_gestion')
uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

print('Usando URI:', uri)

try:
    engine = create_engine(uri)
    with engine.connect() as conn:
        # En SQLAlchemy 2.x, ejecutar SQL crudo requiere `text()`
        result = conn.execute(text('SELECT 1'))
        print('Conexión OK, SELECT 1 ->', result.scalar())
except SQLAlchemyError as e:
    print('Error de SQLAlchemy:', str(e))
except Exception as e:
    print('Error:', str(e))
