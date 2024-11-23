from dash import Dash, html, dcc, Input, Output, State, ctx
import dash_bootstrap_components as dbc
from src.etl import cargar_datos
from src.graphics import graficar_barras, graficar_pie
import os

# Define el estilo de fuente de Spotify
spotify_font = {    
    "font-family": "Gotham",  # Fuente similar a la de Spotify
    "font-size": "24px",  # Tamaño grande
    "background-color": "#1DB954",  # Verde Spotify
    "border-radius": "50px",  # Forma ovalada
    "text-align": "center",
    "padding": "15px 30px",  # Espaciado interno
    "margin": "0 auto",  # Centrado horizontal
    "display": "block"  # Centrado en la columna
}

colores_generos = {
    "Pop": "#F4A7B9",
    "Reggaeton": "#800080",
    "Rock & Indie": "#8B0000",
    "Hip hop": "#000000",
    "Jazz, Soul & Blues": "#000080",
    "EDM & Disco": "#87CEEB",
    "Reggae": "#006400",
    "Flamenco": "#FF0000",
    "Country": "#8B4513",
    "Música clásica": "#9ACD32",
    "Otros": "#808080"
}

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

ruta_csv = os.path.join(os.path.dirname(__file__), 'datos_limpios.csv')
datos = cargar_datos(ruta_csv)

# Layout de la página de inicio
pagina_inicio = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1(
                    "¿Tienes ganas de saber qué escuchas en cada estación del año?",
                    className="text-center my-5",
                    style={"color": "#4CAF50"}
                )
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "¡Pincha aquí!",
                    id="boton-inicio",
                    color="success",
                    size="lg",
                    className="w-50 mx-auto d-block",
                    style=spotify_font
                )
            )
        )
    ],
    fluid=True
)

# Layout de la página de análisis
pagina_analisis = dbc.Container(
    [
        dcc.Location(id="url"),  # Componente para manejar el scroll
        dbc.Row(
            dbc.Col(
                html.H1(
                    "Análisis de Preferencia de Géneros por Estaciones",
                    className="text-center my-4",
                    style={"color": "#4CAF50"}
                )
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id="grafico-barras",
                    figure=graficar_barras(datos),
                    className="my-4"
                )
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id="grafico-pie",
                    figure=graficar_pie(datos, colores_generos),
                    className="my-4"
                )
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Conclusión",
                    id="boton-conclusion",
                    color="success",
                    size="lg",
                    className="my-3 shadow-lg",
                    style=spotify_font
                )
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    id="conclusion-texto",
                    className="text-center my-4",
                    style={"padding-top": "100px"}
                )
            )
        ),
        html.Div(id="scroll-target", style={"padding-top": "50px"})  # Marcador para el scroll
    ],
    fluid=True
)

# Layout principal
app.layout = html.Div(
    id="layout-principal",
    children=[pagina_inicio],
    style={
        "background-color": "#000",
        "color": "#fff",
        "min-height": "100vh",
        "padding": "20px"
    }
)

# Callback para cambiar de página
@app.callback(
    Output("layout-principal", "children"),
    Input("boton-inicio", "n_clicks")
)
def cambiar_pagina(n_clicks):
    if n_clicks:
        return pagina_analisis
    return pagina_inicio

# Callback para mostrar la conclusión al pulsar el botón y realizar scroll
@app.callback(
    [
        Output("conclusion-texto", "children"),
        Output("conclusion-texto", "style"),
        Output("url", "href")
    ],
    Input("boton-conclusion", "n_clicks"),
    prevent_initial_call=True
)
def mostrar_conclusion(n_clicks):
    if n_clicks is None or n_clicks == 0:
        return None, {"opacity": "0"}, None
    try:
        genero_verano = datos[datos["Estación"] == "Verano"]["Género General"].mode()[0]
        genero_otoño = datos[datos["Estación"] == "Otoño"]["Género General"].mode()[0]
        genero_invierno = datos[datos["Estación"] == "Invierno"]["Género General"].mode()[0]
        genero_primavera = datos[datos["Estación"] == "Primavera"]["Género General"].mode()[0]
    except KeyError as e:
        return f"Error en los datos: {e}", {"opacity": "0"}, None

    conclusion = html.Div(
        [
            html.P(f"En verano tu género más escuchado es {genero_verano}", style=spotify_font),
            html.P(f"En otoño tu género más escuchado es {genero_otoño}", style=spotify_font),
            html.P(f"En invierno tu género más escuchado es {genero_invierno}", style=spotify_font),
            html.P(f"En primavera tu género más escuchado es {genero_primavera}", style=spotify_font)
        ]
    )
    return conclusion, {"opacity": "1"}, "#scroll-target"  # Realiza scroll hasta el marcador

if __name__ == "__main__":
    app.run_server(debug=True)