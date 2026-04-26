# prueba_clima.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import date
from app.services.clima import buscar_coordenadas, obtener_clima
from app.services.prediccion import (
    calcular_etapa,
    calcular_desviaciones,
    detectar_eventos,
    generar_reporte,
)

# ── 1 y 2. Coordenadas y clima real ───────────────────────────
coords   = buscar_coordenadas("Tehuacán")
clima_raw = obtener_clima(coords["lat"], coords["lon"])

# Sobreescribimos el clima real con valores críticos simulados
clima_actual = {
    "temperature_2m":        38.5,   # por encima del máximo del cultivo
    "relative_humidity_2m":  88.0,   # humedad muy alta → riesgo hongo
    "precipitation":         25.0,   # lluvia intensa → asfixia radicular
    "wind_speed_10m":        40.0,
}

# ── 3. Cultivo en etapa crítica (Floración) ───────────────────
idoneo = {
    "temp_max_c":       35.0,   # temp actual (38.5) supera este límite
    "temp_min_c":       10.0,
    "humedad_relativa": 60.0,   # humedad actual (88%) supera este límite
}
cultivo = {
    "nombre":               "Maíz Grano",
    "dias_siembra_cosecha": 150,
}
importancia = "Alta"

# Fecha de siembra ajustada para que el cultivo esté al 65% → Floración
# 65% de 150 días = 97.5 días atrás
from datetime import timedelta
fecha_siembra = date.today() - timedelta(days=98)

# ── 4. Cálculos ───────────────────────────────────────────────
print("=== ETAPA DEL CULTIVO ===")
etapa = calcular_etapa(fecha_siembra, cultivo["dias_siembra_cosecha"])
print(etapa)

print("\n=== DESVIACIONES ===")
desv = calcular_desviaciones(clima_actual, idoneo)
print(desv)

print("\n=== EVENTOS DETECTADOS ===")
eventos = detectar_eventos(desv, etapa)
print(eventos)

print("\n=== REPORTE FINAL ===")
reporte = generar_reporte(
    cultivo["nombre"], etapa, desv, eventos, importancia
)
for clave, valor in reporte.items():
    print(f"  {clave}: {valor}")