"""
Módulo de datos: obtiene información del entorno en tiempo real.
Responsable: Igor
"""

import requests
from datetime import datetime, timezone, timedelta


def obtener_datos():
    """
    Obtiene los datos actuales del entorno.
    
    Retorna:
        dict: {temperatura, hora, dia_semana, estacion}
    """
    # Obtener temperatura desde API de Open-Meteo (Coordenadas de Trujillo, Perú)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -8.1172824,   # Latitud de Trujillo, Perú
        "longitude": -79.0385701,  # Longitud de Trujillo, Perú
        "current_weather": True
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        weather = response.json().get("current_weather", {})
        temperatura = weather.get("temperature", 25.0)
    except Exception:
        temperatura = 25.0  # fallback si falla la API

    # Obtener datos temporales en zona horaria de Perú (UTC-5)
    # Perú no usa horario de verano, siempre es UTC-5
    zona_horaria_peru = timezone(timedelta(hours=-5))
    ahora = datetime.now(zona_horaria_peru)
    hora = ahora.hour
    dia_semana = ahora.strftime("%A")

    # Determinar estación del año
    mes = ahora.month
    if mes in [12, 1, 2]:
        estacion = "Verano"
    elif mes in [3, 4, 5]:
        estacion = "Otoño"
    elif mes in [6, 7, 8]:
        estacion = "Invierno"
    else:
        estacion = "Primavera"

    return {
        "temperatura": temperatura,
        "hora": hora,
        "dia_semana": dia_semana,
        "estacion": estacion
    }
