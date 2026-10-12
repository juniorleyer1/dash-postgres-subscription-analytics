from sqlalchemy import create_engine, text
import pandas as pd


DB_CONFIG = {
    "database": "videosubs_db",
    "user": "alumno",
    "password": "123456",
    "host": "localhost",
    "port": "5432",
}

# 1. Crear el string de conexión para PostgreSQL (usando psycopg2)
connection_url = f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# 2. Crear el engine de SQLAlchemy
engine = create_engine(connection_url)

_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(connection_url, pool_pre_ping=True)
    return _engine

def read_sql_df(sql: str, params: dict | None = None) -> pd.DataFrame:
    with get_engine().connect() as conn:
        return pd.read_sql(text(sql), conn, params=params or {})




# source venv/Scripts/activate
# deactivate