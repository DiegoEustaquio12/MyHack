# app/services/prediccion.py
from datetime import date


def calcular_etapa(fecha_siembra: date, dias_siembra_cosecha: int) -> dict:
    hoy = date.today()
    dias_transcurridos = max(0, (hoy - fecha_siembra).days)

    porcentaje = 0
    if dias_siembra_cosecha and dias_siembra_cosecha > 0:
        porcentaje = (dias_transcurridos / dias_siembra_cosecha) * 100

    if porcentaje <= 20:
        etapa = "Germinación"
    elif porcentaje <= 50:
        etapa = "Crecimiento"
    elif porcentaje <= 80:
        etapa = "Floración"
    else:
        etapa = "Maduración"

    return {
        "dias_transcurridos": dias_transcurridos,
        "porcentaje":         round(porcentaje, 1),
        "etapa":              etapa,
        "es_critica":         40 <= porcentaje <= 80,
    }


def calcular_desviaciones(clima_actual: dict, idoneo: dict) -> dict:
    temp    = clima_actual["temperature_2m"]
    humedad = clima_actual["relative_humidity_2m"]
    lluvia  = clima_actual["precipitation"]

    return {
        "temp":          temp,
        "humedad":       humedad,
        "lluvia":        lluvia,
        "delta_calor":   round(temp - idoneo["temp_max_c"], 2),
        "delta_frio":    round(idoneo["temp_min_c"] - temp, 2),
        "delta_humedad": round(humedad - idoneo["humedad_relativa"], 2),
    }


def detectar_eventos(desv: dict, etapa: dict,
                     temp_max_dia: float = None,
                     temp_min_dia: float = None) -> list:
    """
    temp_max_dia y temp_min_dia son opcionales: permiten detectar
    Choque Térmico cuando se tienen datos del pronóstico diario.
    """
    eventos = set()
    temp    = desv["temp"]
    humedad = desv["humedad"]
    lluvia  = desv["lluvia"]

    # ── Eventos simples ───────────────────────────────────────
    if desv["delta_calor"] > 0:
        eventos.add("Evento Calor")

    if desv["delta_frio"] > 0:
        eventos.add("Evento Frío")

    if desv["delta_humedad"] < 0:
        eventos.add("Déficit de Humedad")

    if humedad > 85:
        eventos.add("Exceso de Humedad")

    if lluvia == 0 and humedad < 40:
        eventos.add("Evento Sequía")

    # ── Choque Térmico (oscilación extrema en 24h) ────────────
    if temp_max_dia is not None and temp_min_dia is not None:
        oscilacion = temp_max_dia - temp_min_dia
        if oscilacion > 20:
            eventos.add("Choque Térmico")

    # ── Eventos combinados ────────────────────────────────────
    # Estrés Hídrico Agudo: calor alto + humedad baja < 40%
    if "Evento Calor" in eventos and humedad < 40:
        eventos.add("Estrés Hídrico")

    # Riesgo de Hongo: temp > 22°C + humedad > humedad_relativa óptima
    if temp > 22 and "Exceso de Humedad" in eventos:
        eventos.add("Riesgo de Hongo")

    # Aborto de Floración: etapa crítica + calor extremo
    if etapa["es_critica"] and "Evento Calor" in eventos:
        eventos.add("Aborto de Floración")

    # Cosecha en Riesgo: floración + calor
    if etapa["etapa"] == "Floración" and desv["delta_calor"] > 0:
        eventos.add("Cosecha en Riesgo")

    # Asfixia Radicular: lluvia intensa + humedad muy alta
    if lluvia > 20 and humedad > 90:
        eventos.add("Asfixia Radicular")

    # Retraso de Ciclo: frío en etapa temprana
    if "Evento Frío" in eventos and etapa["etapa"] in ("Germinación", "Crecimiento"):
        eventos.add("Retraso de Ciclo")

    # Eliminar redundancias: si hay Estrés Hídrico, Déficit de Humedad es redundante
    if "Estrés Hídrico" in eventos:
        eventos.discard("Déficit de Humedad")
    if "Asfixia Radicular" in eventos:
        eventos.discard("Exceso de Humedad")
    if "Aborto de Floración" in eventos:
        eventos.discard("Evento Calor")

    return list(eventos)