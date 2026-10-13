from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from config import engine, read_sql_df
import plotly.graph_objects as go

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
SELECT 
    CASE 
        WHEN was_subscription_paid = TRUE THEN 'Pagado'
        ELSE 'No pagado'
    END AS estado_pago,
    COUNT(*) AS cantidad
FROM 
    subscription_cohorts
GROUP BY 
    was_subscription_paid;
"""

# estado de los ingresos por mes
query6 = """SELECT 
    CASE 
            WHEN was_subscription_paid = TRUE THEN 'Pagado'
            ELSE 'No pagado'
        END AS estado_pago,
    DATE_TRUNC('month', created_date) AS mes,
    COUNT(*) AS cantidad,
    SUM(subscription_cost) AS ingresos_totales
FROM 
    subscription_cohorts
GROUP BY 
    DATE_TRUNC('month', created_date), 
    was_subscription_paid
ORDER BY 
    mes ASC, 
    was_subscription_paid DESC;
"""

ingresos_totales = read_sql_df(sql=query1)
suscripciones_totales = read_sql_df(sql=query2)
intervalo_suscripcion = read_sql_df(sql=query4)
suscripciones_mensuales = read_sql_df(sql=query3)
per_suscripciones = read_sql_df(sql=query5)
estado_suscripciones_mm = read_sql_df(sql=query6)

app = Dash(__name__)
app.title = "KPIs"

fig = px.line(suscripciones_mensuales, x="mes", y="nuevas_suscripciones",
            title="Suscripciones por Mes")
fig.update_yaxes(matches=None)

fig2 = px.pie(per_suscripciones, values='cantidad',
            names='estado_pago', title="Suscripciones Pagadas vs No Pagadas")

fig3 = px.area(estado_suscripciones_mm, x="mes", y="cantidad",
            color="estado_pago", line_group="estado_pago", title="Estado de las Suscripciones por mes")

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

    html.Div(
        children=[
            # Gráfico 1
            html.Div(
                [dcc.Graph(figure=fig, id="grafico-demo")],
                style={"flex": "1", "maxWidth": "600px", "padding": "16px"},
            ),
            # Gráfico 2
            html.Div(
                [dcc.Graph(figure=fig2, id="grafico-demo2")],
                style={"flex": "1", "maxWidth": "600px", "padding": "16px"},
            ),
        ],
        style={
            "display": "flex",
            "flexDirection": "row",  # Esto los alinea en fila horizontal
            "flexWrap": "wrap",  # Permite que bajen si la pantalla es muy pequeña
            "justifyContent": "center",  # Los centra horizontalmente
            "alignItems": "center",  # Los alinea verticalmente
        },
    ),

    html.Div(
        [dcc.Graph(figure=fig3, id="grafico-demo5")],
    ),

])


@app.callback(
    [
        Output("kpi-total", "children"),
        Output("kpi-totalsus", "children"),
        Output("kpi-intersus", "children")
    ]
)
def actualizar_kpis():
    total_ventas = ingresos_totales["total"].iloc[0]
    texto_ventas = f"${total_ventas:,.2f}" 

    total_suscriptores = suscripciones_totales["susc"].iloc[0] 
    texto_suscriptores = f"{total_suscriptores:,}"

    mayor_intervalo = intervalo_suscripcion["interval"].iloc[0]

    return texto_ventas, texto_suscriptores, mayor_intervalo


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8050, debug=True)
    # print(df1["total"])
    # print(df2["susc"])
    # print(df3["interval"])
    # print(df6)
