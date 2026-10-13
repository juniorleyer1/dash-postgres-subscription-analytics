from dash import Dash, html, dcc, Input, Output
import plotly.express as px
from config import read_sql_df

# --- CONSULTAS SQL ---
query1 = "SELECT SUM(subscription_cost) as total FROM subscription_cohorts WHERE was_subscription_paid = TRUE;"
query2 = "SELECT count(distinct customer_id) as susc from subscription_cohorts where was_subscription_paid = TRUE;"
query3 = """
SELECT DATE_TRUNC('month', created_date) AS mes, COUNT(*) AS nuevas_suscripciones
FROM subscription_cohorts
GROUP BY mes
ORDER BY mes;
"""
query4 = """SELECT subscription_interval as interval, SUM(subscription_cost) AS ingresos_totales
FROM subscription_cohorts
WHERE was_subscription_paid = TRUE
GROUP BY subscription_interval;
"""
query5 = """
SELECT 
    CASE 
        WHEN was_subscription_paid = TRUE THEN 'Pagado'
        ELSE 'No pagado'
    END AS estado_pago,
    COUNT(*) AS cantidad
FROM subscription_cohorts
GROUP BY was_subscription_paid;
"""
query6 = """SELECT 
    CASE 
        WHEN was_subscription_paid = TRUE THEN 'Pagado'
        ELSE 'No pagado'
    END AS estado_pago,
    DATE_TRUNC('month', created_date) AS mes,
    COUNT(*) AS cantidad,
    SUM(subscription_cost) AS ingresos_totales
FROM subscription_cohorts
GROUP BY DATE_TRUNC('month', created_date), was_subscription_paid
ORDER BY mes ASC, was_subscription_paid DESC;
"""

ingresos_totales = read_sql_df(sql=query1)
suscripciones_totales = read_sql_df(sql=query2)
intervalo_suscripcion = read_sql_df(sql=query4)
suscripciones_mensuales = read_sql_df(sql=query3)
per_suscripciones = read_sql_df(sql=query5)
estado_suscripciones_mm = read_sql_df(sql=query6)

app = Dash(__name__)
app.title = "KPIs Dashboard"

# --- CONFIGURACIÓN DE GRÁFICOS CON ESTILO LIMPIO ---
fig = px.line(suscripciones_mensuales, x="mes", y="nuevas_suscripciones", title="Suscripciones por Mes")
fig.update_layout(template="plotly_white", margin=dict(t=40, b=20, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")

fig2 = px.pie(per_suscripciones, values='cantidad', names='estado_pago', title="Suscripciones Pagadas vs No Pagadas", hole=0.4)
fig2.update_layout(template="plotly_white", margin=dict(t=40, b=20, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")

fig3 = px.area(estado_suscripciones_mm, x="mes", y="cantidad", color="estado_pago", line_group="estado_pago", title="Estado de las Suscripciones por mes")
fig3.update_layout(template="plotly_white", margin=dict(t=40, b=20, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")


# --- LAYOUT DE LA APLICACIÓN ---
app.layout = html.Div(className="container", children=[
    
    # Encabezado
    html.Div(className="header", children=[
        html.H1("MÉTRICAS DE SUSCRIPCIONES", className="title"),
        html.P("Panel de control y métricas de suscripciones", className="subtitle"),
    ]),

    # Tarjetas KPI
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
            html.Div("Mayor intervalo de suscripción", className="kpi-label"),
            html.Div(id="kpi-intersus", className="kpi-value"),
        ]),
    ]),

    # Fila superior de gráficos (2 columnas usando las clases del CSS)
    html.Div(className="charts-grid", children=[
        html.Div(className="chart-card", children=[
            dcc.Graph(figure=fig, config={'displayModeBar': False})
        ]),
        html.Div(className="chart-card", children=[
            dcc.Graph(figure=fig2, config={'displayModeBar': False})
        ]),
    ]),

    # Fila inferior de gráficos (Gráfico de área abarcando todo el ancho)
    html.Div(className="charts-grid", children=[
        html.Div(className="chart-card chart-card-full", children=[
            dcc.Graph(figure=fig3, config={'displayModeBar': False})
        ]),
    ]),

])

# --- CALLBACKS ---
@app.callback(
    [
        Output("kpi-total", "children"),
        Output("kpi-totalsus", "children"),
        Output("kpi-intersus", "children")
    ],
    Input("kpi-total", "id") # Callback de carga inicial
)

def actualizar_kpis(_):
    total_ventas = ingresos_totales["total"].iloc[0] if not ingresos_totales.empty else 0
    texto_ventas = f"${total_ventas:,.2f}" 

    total_suscriptores = suscripciones_totales["susc"].iloc[0] if not suscripciones_totales.empty else 0
    texto_suscriptores = f"{total_suscriptores:,}"

    mayor_intervalo = intervalo_suscripcion["interval"].iloc[0] if not intervalo_suscripcion.empty else "N/A"

    return texto_ventas, texto_suscriptores, mayor_intervalo


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8050, debug=True)