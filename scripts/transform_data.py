from pathlib import Path
import sys
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

# 1. Configurar la ruta raíz para poder importar 'config' desde la carpeta principal
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from config import get_engine, read_sql_df  # Asegúrate de que importe bien tu archivo config.py


def execute_sql(sql: str, params: dict | None = None) -> None:
    """
    Ejecuta sentencias SQL que no devuelven datos (como ALTER, UPDATE, DELETE, DROP)
    utilizando transacciones automáticas y manejo de errores.
    """
    try:
        # .begin() abre la conexión, hace commit automático si todo sale bien, 
        # o hace rollback automático si ocurre algún fallo.
        with get_engine().begin() as conn:
            conn.execute(text(sql), params or {})
        print("¡Operación SQL ejecutada exitosamente!")
        
    except SQLAlchemyError as e:
        print(f"Error de base de datos: {e}")
        raise
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        raise

# --- Ejemplo de cómo usarla ---
if __name__ == "__main__":
    # Tu consulta SQL para modificar la tabla
    query = """
    ALTER TABLE subscription_cohorts
    ALTER COLUMN customer_id TYPE INTEGER USING customer_id::INTEGER,
    ALTER COLUMN created_date TYPE DATE USING created_date::DATE,
    ALTER COLUMN canceled_date TYPE DATE USING canceled_date::DATE,
    ALTER COLUMN subscription_cost TYPE NUMERIC(10, 2) USING subscription_cost::NUMERIC,
    ALTER COLUMN subscription_interval TYPE TEXT USING subscription_interval::TEXT,
    ALTER COLUMN was_subscription_paid TYPE BOOLEAN USING 
        CASE 
            WHEN was_subscription_paid::TEXT ILIKE 'yes' THEN TRUE 
            ELSE FALSE 
        END;
    """
    
    # Ejecutas la función pasándole la consulta
    execute_sql(query)
    
    # query = """
    # SELECT * FROM subscription_cohorts;
    # """
    
    # df = read_sql_df(sql=query)
    # print(df.dtypes)
