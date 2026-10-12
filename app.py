from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from config import engine, read_sql_df


# ingresos totales
query1 = """
SELECT SUM(subscription_cost) as total FROM subscription_cohorts WHERE was_subscription_paid = TRUE;
"""
# total de suscriptores
query2 = """
SELECT count(distinct customer_id) as susc from subscription_cohorts where was_subscription_paid = TRUE;
"""

# evolucion de suscripciones mes a mes
query3 = """
SELECT DATE_TRUNC('month', created_date) AS mes, COUNT(*) AS nuevas_suscripciones
FROM subscription_cohorts
GROUP BY mes
ORDER BY mes;
"""

# ingresos por intervalo de suscripcion
query4 = """SELECT subscription_interval as interval, SUM(subscription_cost) AS ingresos_totales
FROM subscription_cohorts
WHERE was_subscription_paid = TRUE
GROUP BY subscription_interval;
"""

# porcentaje de suscripcion pagadas vs no pagadas
query5 = """
SELECT was_subscription_paid, COUNT(*) AS cantidad
FROM subscription_cohorts
GROUP BY was_subscription_paid;
"""
df1 = read_sql_df(sql=query1)

df2 = read_sql_df(sql=query2)

df3 = read_sql_df(sql=query4)


app = Dash(__name__)
app.title = "KPIs"

app.layout = html.Div(className="container", children=[
    # Encabezado
    html.Div(className="header", children=[
        html.H1("KPIs del periodo", className="title"),
        html.P("Tabla de KPIs", className="subtitle"),
    ]),


    # Tarjetas KPI (solo texto)
    html.Div(className="kpis", children=[
        html.Div(className="kpi-card", children=[
            html.Div("Ventas Totales", className="kpi-label"),
            html.Div(id="kpi-total", className="kpi-value"),
        ]),
        html.Div(className="kpi-card", children=[
            html.Div("Suscriptores Totales", className="kpi-label"),
            html.Div(id="kpi-totalsus", className="kpi-value"),
        ]),
        html.Div(className="kpi-card", children=[
            html.Div("Mayor intervalo de suscripcion", className="kpi-label"),
            html.Div(id="kpi-intersus", className="kpi-value"),
        ]),
    ]),
])

@app.callback(
    [
        Output("kpi-total", "children"),
        Output("kpi-totalsus", "children"),
        Output("kpi-intersus", "children")
    ]
)
def actualizar_kpis():
    # 1. Extraer el valor de ventas totales (ej: sumando la columna de costo)
    # Asumiendo que df1 tiene una columna con los montos o costos
    total_ventas = df1["total"].iloc[0]
    texto_ventas = f"${total_ventas:,.2f}" # Formato de dinero bonito

    # 2. Extraer suscriptores totales (ej: conteo de clientes únicos o filas)
    total_suscriptores = df2["susc"].iloc[0] # o len(df2)
    texto_suscriptores = f"{total_suscriptores:,}"

    # 3. Mayor intervalo de suscripción
    # Asumiendo que df3 tiene el resultado de la consulta del intervalo más repetido
    mayor_intervalo = df3["interval"].iloc[0]

    return texto_ventas, texto_suscriptores, mayor_intervalo

if __name__ == "__main__":
    # print(df1["total"])
    # print(df2["susc"])
    # print(df3["interval"])
    app.run(host="127.0.0.1", port=8050, debug=True)
