import requests

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL  = "https://geocoding-api.open-meteo.com/v1/search"

def buscar_coordenadas(nombre_ciudad):
    """Recibe 'Puebla' o 'Tehuacán' y devuelve lat, lon, nombre oficial."""
    r = requests.get(GEOCODING_URL, params={
        "name":     nombre_ciudad,
        "count":    1,
        "language": "es",
        "format":   "json",
    }, timeout=10)
    r.raise_for_status()

    resultados = r.json().get("results")
    if not resultados:
        return None  # ciudad no encontrada

    ciudad = resultados[0]
    return {
        "nombre":   ciudad["name"],
        "lat":      ciudad["latitude"],
        "lon":      ciudad["longitude"],
        "pais":     ciudad.get("country", ""),
        "region":   ciudad.get("admin1", ""),   # estado/provincia
    }

def obtener_clima(lat, lon):
    params = {
        "latitude":  lat,
        "longitude": lon,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m",
        ],
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
        ],
        "timezone":     "America/Mexico_City",
        "forecast_days": 7,
    }
    r = requests.get(OPEN_METEO_URL, params=params, timeout=10)
    r.raise_for_status()
    return r.json()