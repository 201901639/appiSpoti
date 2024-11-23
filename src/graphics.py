# graphics.py
import plotly.express as px

def aplicar_tema_oscuro(fig):
    fig.update_layout(
        paper_bgcolor="#000",
        plot_bgcolor="#000",
        font=dict(color="#fff")
    )
    return fig

def graficar_barras(datos):
    """Genera un gráfico de barras usando Plotly Express con colores personalizados."""
    # Definir colores personalizados para las estaciones
    colores_estaciones = {
        'Otoño': '#8B4513',
        'Invierno': '#87CEEB',
        'Verano': '#FFD700',
        'Primavera': '#9ACD32'
    }
    
    # Agrupar los datos por género y estación
    genre_season_count = datos.groupby(['Género General', 'Estación']).size().reset_index(name='Count')
    
    # Crear el gráfico de barras
    fig = px.bar(
        genre_season_count,
        x='Género General',
        y='Count',
        color='Estación',
        title='Número de canciones escuchadas por género y estación',
        labels={'Género General': 'Género', 'Count': 'Número de Canciones'},
        color_discrete_map=colores_estaciones  # Aplicar colores personalizados
    )
    
    # Ajustar diseño del gráfico
    fig.update_layout(barmode='group', xaxis_tickangle=-45)

    fig = aplicar_tema_oscuro(fig)
    return fig

def graficar_pie(datos, colores_generos):
    """Genera un gráfico de pastel con colores personalizados."""
    generos_estacion = datos.groupby('Género General').size().reset_index(name='Count')
    fig = px.pie(
        generos_estacion,
        names='Género General',
        values='Count',
        title='Distribución de Géneros del Usuario',
        color='Género General',
        color_discrete_map=colores_generos
    )
    fig.update_traces(textinfo='percent+label')
    fig = aplicar_tema_oscuro(fig)
    return fig