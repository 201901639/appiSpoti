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
    "display": "block",  # Centrado en la columna
    "color": "#000",  # Texto en negro
    "font-weight": "bold"  # Texto en negrita
}

style_text = {
    'color': 'green',  # Color del texto en verde
    'background-color': 'transparent',  # Sin fondo
    'font-family': 'Gotham, sans-serif',  # Fuente Gotham
    'font-size': '22px',  # Tamaño de la fuente (ajústalo a lo que prefieras)
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
server = app.server

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

# Formulario para recomendaciones
formulario_recomendaciones = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H4("Selecciona tus preferencias:", className="text-center my-4")
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="dropdown-estacion",
                        options=[
                            {"label": "Verano", "value": "Verano"},
                            {"label": "Otoño", "value": "Otoño"},
                            {"label": "Invierno", "value": "Invierno"},
                            {"label": "Primavera", "value": "Primavera"}
                        ],
                        placeholder="¿En qué estación te encuentras?",
                        className="mb-4"
                    ),
                    width=6
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="dropdown-genero",
                        options=[
                            {"label": genero, "value": genero}
                            for genero in datos["Género General"].unique()
                        ],
                        placeholder="¿Qué género te apetece escuchar hoy?",
                        className="mb-4"
                    ),
                    width=6
                )
            ]
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Mostrar recomendaciones",
                    id="boton-recomendaciones",
                    color="primary",
                    size="lg",
                    className="my-3",
                    style=spotify_font
                )
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    id="output-recomendaciones",
                    className="text-center my-4",
                    style={"color": "#fff", "font-size": "18px"}
                )
            )
        )
    ]
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
        formulario_recomendaciones,
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
            html.P(f"En verano tu género más escuchado es {genero_verano}", style=style_text),
            html.P(f"En otoño tu género más escuchado es {genero_otoño}", style=style_text),
            html.P(f"En invierno tu género más escuchado es {genero_invierno}", style=style_text),
            html.P(f"En primavera tu género más escuchado es {genero_primavera}", style=style_text)
        ]
    )
    return conclusion, {"opacity": "1"}, "#scroll-target"  # Realiza scroll hasta el marcador
@app.callback(
    Output("output-recomendaciones", "children"),
    [
        Input("boton-recomendaciones", "n_clicks"),
        State("dropdown-estacion", "value"),
        State("dropdown-genero", "value")
    ]
)
def generar_recomendaciones(n_clicks, estacion, genero):
    if not n_clicks or not estacion or not genero:
        return "Selecciona ambos campos para ver las recomendaciones."
    
    # Filtrar el dataset por estación y género
    recomendaciones = datos[
        (datos["Estación"] == estacion) & (datos["Género General"] == genero)
    ]
    
    if recomendaciones.empty:
        return f"No hay canciones disponibles para {genero} en {estacion}."
    
    # Seleccionar las primeras 5 canciones
    canciones = recomendaciones["Nombres"].head(5).tolist()
    
    return html.Ul([html.Li(cancion, style={"color": "green"}) for cancion in canciones])

if __name__ == "__main__":
    app.run_server(debug=True)