# prueba_clima.py
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import date, timedelta
from app.services.clima import buscar_coordenadas, obtener_clima
from app.services.prediccion import calcular_etapa, calcular_desviaciones, detectar_eventos
from app.services.soluciones import generar_salida_completa

SEP = "\n" + "="*60 + "\n"

def correr_caso(nombre_caso, municipio, cultivo, idoneo,
                clima_simulado, importancia, dias_atras,
                temp_max_dia=None, temp_min_dia=None):

    print(SEP + f"CASO: {nombre_caso}" + SEP)

    fecha_siembra = date.today() - timedelta(days=dias_atras)
    etapa   = calcular_etapa(fecha_siembra, cultivo["dias_siembra_cosecha"])
    desv    = calcular_desviaciones(clima_simulado, idoneo)
    eventos = detectar_eventos(desv, etapa, temp_max_dia, temp_min_dia)
    salida  = generar_salida_completa(
        municipio, cultivo["nombre"], etapa, desv, eventos, importancia
    )

    print(f"  Municipio    : {salida['municipio']}")
    print(f"  Cultivo      : {salida['cultivo']}")
    print(f"  Etapa        : {salida['etapa']} ({salida['porcentaje']}%)")
    print(f"  Puntaje      : {salida['puntaje']} pts")
    print(f"  Nivel riesgo : {salida['nivel_riesgo']} ({salida['color'].upper()})")
    print(f"  Urgencia     : {salida['urgencia']}")
    print(f"\n  Diagnóstico:\n  {salida['diagnostico']}\n")
    print(f"  Eventos: {salida['eventos']}\n")

    for s in salida["soluciones"]:
        print(f"  [{s['urgencia']}] {s['evento']}")
        for a in s["acciones"]:
            print(f"    • {a}")
        print(f"    Ref: {s['referencia']}")
        print()


# ── CASO 1: Estrés hídrico agudo (calor + sequía) ────────────
correr_caso(
    nombre_caso    = "Estrés hídrico agudo — Maíz en Crecimiento",
    municipio      = "Tecamachalco",
    cultivo        = {"nombre": "Maíz Grano", "dias_siembra_cosecha": 150},
    idoneo         = {"temp_max_c": 35.0, "temp_min_c": 10.0, "humedad_relativa": 60.0},
    clima_simulado = {"temperature_2m": 39.0, "relative_humidity_2m": 28.0,
                      "precipitation": 0.0,  "wind_speed_10m": 20.0},
    importancia    = "Alta",
    dias_atras     = 55,
)

# ── CASO 2: Riesgo de hongo (calor + humedad alta) ────────────
correr_caso(
    nombre_caso    = "Proliferación fúngica — Frijol en Floración",
    municipio      = "Cuyoaco",
    cultivo        = {"nombre": "Frijol", "dias_siembra_cosecha": 130},
    idoneo         = {"temp_max_c": 27.0, "temp_min_c": 15.0, "humedad_relativa": 65.0},
    clima_simulado = {"temperature_2m": 26.0, "relative_humidity_2m": 91.0,
                      "precipitation": 8.0,  "wind_speed_10m": 5.0},
    importancia    = "Alta",
    dias_atras     = 80,
)

# ── CASO 3: Aborto de floración (etapa crítica + calor) ───────
correr_caso(
    nombre_caso    = "Aborto de floración — Maíz en Floración",
    municipio      = "Cholula",
    cultivo        = {"nombre": "Maíz Grano", "dias_siembra_cosecha": 150},
    idoneo         = {"temp_max_c": 35.0, "temp_min_c": 10.0, "humedad_relativa": 60.0},
    clima_simulado = {"temperature_2m": 38.5, "relative_humidity_2m": 88.0,
                      "precipitation": 25.0, "wind_speed_10m": 40.0},
    importancia    = "Alta",
    dias_atras     = 98,
)

# ── CASO 4: Choque térmico (oscilación > 20°C en 24h) ────────
correr_caso(
    nombre_caso    = "Choque térmico — Papa en Crecimiento",
    municipio      = "Chalchicomula",
    cultivo        = {"nombre": "Papa", "dias_siembra_cosecha": 110},
    idoneo         = {"temp_max_c": 20.0, "temp_min_c": 8.0, "humedad_relativa": 70.0},
    clima_simulado = {"temperature_2m": 18.0, "relative_humidity_2m": 55.0,
                      "precipitation": 0.0,  "wind_speed_10m": 8.0},
    importancia    = "Baja",
    dias_atras     = 35,
    temp_max_dia   = 32.0,   # oscilación de 27°C → Choque Térmico
    temp_min_dia   = 5.0,
)

# ── CASO 5: Condiciones óptimas ───────────────────────────────
correr_caso(
    nombre_caso    = "Condiciones óptimas — Trigo en Crecimiento",
    municipio      = "Libres",
    cultivo        = {"nombre": "Trigo Grano", "dias_siembra_cosecha": 140},
    idoneo         = {"temp_max_c": 22.0, "temp_min_c": 3.0, "humedad_relativa": 55.0},
    clima_simulado = {"temperature_2m": 17.0, "relative_humidity_2m": 60.0,
                      "precipitation": 5.0,  "wind_speed_10m": 10.0},
    importancia    = "Alta",
    dias_atras     = 50,
)