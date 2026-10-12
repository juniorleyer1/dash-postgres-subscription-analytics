import pandas as pd
from pathlib import Path
import sys

from sqlalchemy import text

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from config import read_sql_df  # Asegúrate de que importe bien tu archivo config.py


query = """
select subscription_interval from subscription_cohorts
"""

query2 = """
SELECT DISTINCT subscription_interval 
FROM subscription_cohorts;
"""
df = read_sql_df(query2)
print(df)
# print(df.isna().sum())
# print("muestra de valores nulos".center(50, "-"))
# activos = df[df["canceled_date"].isna()]
# print(activos.head())