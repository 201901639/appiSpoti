# etl.py
import pandas as pd

def cargar_datos(ruta_csv):
    """Carga el archivo datos_limpios.csv y realiza transformaciones necesarias."""
    try:
        datos = pd.read_csv(ruta_csv)
        # Asegúrate de que la columna 'Fecha' esté en formato datetime
        datos['Fecha en la que se añadió'] = pd.to_datetime(datos['Fecha en la que se añadió'])
        return datos
    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo {ruta_csv} no se encuentra.")
