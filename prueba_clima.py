# prueba_clima.py
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import date, timedelta
from app.services.clima import buscar_coordenadas, obtener_clima
from app.services.prediccion import calcular_etapa, calcular_desviaciones, detectar_eventos
from app.services.soluciones import generar_salida_completa

SEP = "\n" + "="*55 + "\n"

def correr_caso(nombre_caso, municipio, cultivo, idoneo, clima_simulado,
                importancia, dias_atras):

    print(SEP + f"CASO: {nombre_caso}" + SEP)

    fecha_siembra = date.today() - timedelta(days=dias_atras)
    etapa   = calcular_etapa(fecha_siembra, cultivo["dias_siembra_cosecha"])
    desv    = calcular_desviaciones(clima_simulado, idoneo)
    eventos = detectar_eventos(desv, etapa)
    salida  = generar_salida_completa(
        municipio, cultivo["nombre"], etapa, desv, eventos, importancia
    )

    print(f"Municipio   : {salida['municipio']}")
    print(f"Cultivo     : {salida['cultivo']}")
    print(f"Etapa       : {salida['etapa']} ({salida['porcentaje']}%)")
    print(f"Puntaje     : {salida['puntaje']} pts")
    print(f"Nivel riesgo: {salida['nivel_riesgo']} ({salida['color'].upper()})")
    print(f"Urgencia    : {salida['urgencia']}")
    print(f"\nDiagnóstico:\n{salida['diagnostico']}")
    print(f"\nEventos detectados: {salida['eventos']}")
    print("\nSoluciones recomendadas:")
    for s in salida["soluciones"]:
        print(f"  [{s['evento']}]")
        print(f"    Acción : {s['accion']}")
        print(f"    Detalle: {s['detalle']}")
        print(f"    Insumos: {s['insumos']}")


# ── CASO 1: Todo en crisis (Floración + calor + lluvia + municipio importante)
correr_caso(
    nombre_caso    = "Crisis total — Maíz en Floración",
    municipio      = "Tecamachalco",
    cultivo        = {"nombre": "Maíz Grano", "dias_siembra_cosecha": 150},
    idoneo         = {"temp_max_c": 35.0, "temp_min_c": 10.0, "humedad_relativa": 60.0},
    clima_simulado = {"temperature_2m": 38.5, "relative_humidity_2m": 88.0,
                      "precipitation": 25.0, "wind_speed_10m": 40.0},
    importancia    = "Alta",
    dias_atras     = 98,   # 65% del ciclo → Floración
)

# ── CASO 2: Sequía severa en Crecimiento
correr_caso(
    nombre_caso    = "Sequía severa — Frijol en Crecimiento",
    municipio      = "Cuyoaco",
    cultivo        = {"nombre": "Frijol", "dias_siembra_cosecha": 130},
    idoneo         = {"temp_max_c": 27.0, "temp_min_c": 15.0, "humedad_relativa": 65.0},
    clima_simulado = {"temperature_2m": 32.0, "relative_humidity_2m": 28.0,
                      "precipitation": 0.0,  "wind_speed_10m": 18.0},
    importancia    = "Alta",
    dias_atras     = 40,   # 30% → Crecimiento
)

# ── CASO 3: Helada en Germinación, municipio secundario
correr_caso(
    nombre_caso    = "Helada temprana — Papa en Germinación",
    municipio      = "Chalchicomula",
    cultivo        = {"nombre": "Papa", "dias_siembra_cosecha": 110},
    idoneo         = {"temp_max_c": 20.0, "temp_min_c": 8.0, "humedad_relativa": 70.0},
    clima_simulado = {"temperature_2m": 4.0,  "relative_humidity_2m": 55.0,
                      "precipitation": 0.0,  "wind_speed_10m": 5.0},
    importancia    = "Baja",
    dias_atras     = 10,   # 9% → Germinación
)

# ── CASO 4: Condiciones óptimas — sin eventos
correr_caso(
    nombre_caso    = "Condiciones óptimas — Trigo en Crecimiento",
    municipio      = "Libres",
    cultivo        = {"nombre": "Trigo Grano", "dias_siembra_cosecha": 140},
    idoneo         = {"temp_max_c": 22.0, "temp_min_c": 3.0, "humedad_relativa": 55.0},
    clima_simulado = {"temperature_2m": 17.0, "relative_humidity_2m": 60.0,
                      "precipitation": 5.0,  "wind_speed_10m": 10.0},
    importancia    = "Alta",
    dias_atras     = 50,   # 35% → Crecimiento
)