from datetime import date

def calcular_etapa(fecha_siembra: date, dias_siembra_cosecha: int) -> dict:
    hoy = date.today()
    dias_transcurridos = max(0, (hoy - fecha_siembra).days)

    if dias_siembra_cosecha and dias_siembra_cosecha > 0:
        porcentaje = (dias_transcurridos / dias_siembra_cosecha) * 100
    else:
        porcentaje = 0

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
        "delta_calor":   temp - idoneo["temp_max_c"],
        "delta_frio":    idoneo["temp_min_c"] - temp,
        "delta_humedad": humedad - idoneo["humedad_relativa"],
    }


def detectar_eventos(desv: dict, etapa: dict) -> list:
    eventos = []
    temp    = desv["temp"]
    humedad = desv["humedad"]
    lluvia  = desv["lluvia"]

    if desv["delta_calor"] > 0:
        eventos.append("Evento Calor")
    if desv["delta_frio"] > 0:
        eventos.append("Evento Frío")
    if lluvia == 0 and humedad < 40:
        eventos.append("Evento Sequía")

    if "Evento Calor" in eventos and humedad < 40:
        eventos.append("Estrés Hídrico")
    if temp > 22 and humedad > 85:
        eventos.append("Riesgo de Hongo")
    if desv["delta_calor"] > 0 and etapa["etapa"] == "Floración":
        eventos.append("Cosecha en Riesgo")

    if etapa["es_critica"]:
        if lluvia > 20:
            if humedad > 85:
                eventos.append("Aborto de Floración")
            else:
                eventos.append("Asfixia Radicular")
        if (desv["delta_calor"] > 0 or desv["delta_frio"] > 0):
            if "Aborto de Floración" not in eventos:
                eventos.append("Aborto de Floración")

    return list(set(eventos))