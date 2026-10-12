import pandas as pd
from config import get_engine

file_path = "data/subscription_cohort.csv"

df_original = pd.read_csv(file_path)
# print(df_original.head())

# (Opcional) Limpieza básica de nombres de columnas (pasar a minúsculas, quitar espacios)
df_original.columns = [col.strip().lower().replace(" ", "_") for col in df_original.columns]
# print(df_original.columns)

# 2. Conectar a PostgreSQL (ajusta usuario, contraseña, puerto y nombre de BD)
# Cadena de conexión: postgresql+psycopg2://usuario:password@host:puerto/nombre_bd
engine = get_engine()

# 3. Volcar el DataFrame como una tabla en PostgreSQL
table_name = "subscription_cohorts"
df_original.to_sql(table_name , con=engine, if_exists="replace", index=False)

print("¡Datos cargados exitosamente en PostgreSQL!")