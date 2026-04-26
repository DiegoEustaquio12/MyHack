# app/services/prediccion.py
from datetime import date

# ── Paso 1 y 2: etapa del cultivo ─────────────────────────────
def calcular_etapa(fecha_siembra: date, dias_siembra_cosecha: int) -> dict:
    """
    Devuelve el porcentaje de avance y el nombre de la etapa.
    Refleja el Cálculo 2 de tu diagrama.
    """
    hoy = date.today()
    dias_transcurridos = (hoy - fecha_siembra).days
    dias_transcurridos = max(0, dias_transcurridos)

    if dias_siembra_cosecha and dias_siembra_cosecha > 0:
        porcentaje = (dias_transcurridos / dias_siembra_cosecha) * 100
    else:
        porcentaje = 0

    if porcentaje <= 20:
        etapa = "Germinación"
    elif porcentaje <= 50:
        etapa = "Crecimiento"
    elif porcentaje <= 80:
        etapa = "Floración"   # etapa CRÍTICA según tu diagrama
    else:
        etapa = "Maduración"

    return {
        "dias_transcurridos": dias_transcurridos,
        "porcentaje":         round(porcentaje, 1),
        "etapa":              etapa,
        "es_critica":         40 <= porcentaje <= 80,
    }


# ── Paso 3: desviaciones (estrés) ─────────────────────────────
def calcular_desviaciones(clima_actual: dict, idoneo: dict) -> dict:
    """
    Delta Calor y Delta Humedad del Cálculo 3.
    clima_actual viene de obtener_clima(), idoneo viene de la DB.
    """
    temp     = clima_actual["temperature_2m"]
    humedad  = clima_actual["relative_humidity_2m"]
    lluvia   = clima_actual["precipitation"]

    return {
        "temp":          temp,
        "humedad":       humedad,
        "lluvia":        lluvia,
        "delta_calor":   temp - idoneo["temp_max_c"],       # > 0 = exceso de calor
        "delta_frio":    idoneo["temp_min_c"] - temp,       # > 0 = demasiado frío
        "delta_humedad": humedad - idoneo["humedad_relativa"],  # negativo = seco
    }


# ── Pasos 4 y 5: detección de eventos ─────────────────────────
def detectar_eventos(desv: dict, etapa: dict) -> list:
    """
    Devuelve lista de eventos detectados según tus Detecciones 4 y 5.
    """
    eventos = []
    temp    = desv["temp"]
    humedad = desv["humedad"]
    lluvia  = desv["lluvia"]

    # Eventos base (Detección 4)
    if desv["delta_calor"] > 0:
        eventos.append("Evento Calor")
    if desv["delta_frio"] > 0:
        eventos.append("Evento Frío")
    if lluvia == 0 and humedad < 40:
        eventos.append("Evento Sequía")

    # Eventos combinados (Detección 5)
    if "Evento Calor" in eventos and humedad < 40:
        eventos.append("Estrés Hídrico")
    if temp > 22 and humedad > 85:
        eventos.append("Riesgo de Hongo")
    if desv["delta_calor"] > 0 and etapa["etapa"] == "Floración":
        eventos.append("Cosecha en Riesgo")

    # Eventos del diagrama de árbol (imagen 1)
    if etapa["es_critica"]:
        if lluvia > 20:                        # precipitación alta
            if humedad > 85:
                eventos.append("Aborto de Floración")
            else:
                eventos.append("Asfixia Radicular")
        if (desv["delta_calor"] > 0 or desv["delta_frio"] > 0):
            if "Aborto de Floración" not in eventos:
                eventos.append("Aborto de Floración")

    return list(set(eventos))   # sin duplicados


# ── Generación de salida final ─────────────────────────────────
PRIORIDADES = {
    "Aborto de Floración": ("Alto",  "Urgente"),
    "Estrés Hídrico":      ("Alto",  "Urgente"),
    "Asfixia Radicular":   ("Alto",  "Alta"),
    "Cosecha en Riesgo":   ("Alto",  "Alta"),
    "Riesgo de Hongo":     ("Medio", "Alta"),
    "Retraso de Ciclo":    ("Medio", "Media"),
    "Evento Calor":        ("Bajo",  "Normal"),
    "Evento Frío":         ("Bajo",  "Normal"),
    "Evento Sequía":       ("Bajo",  "Normal"),
}

def generar_reporte(cultivo_nombre, etapa, desv, eventos, importancia_municipio):
    """
    Une todo y aplica la regla de importancia de municipio_cultivos.
    """
    if not eventos:
        return {
            "cultivo":         cultivo_nombre,
            "etapa":           etapa["etapa"],
            "nivel_riesgo":    "Bajo",
            "prioridad":       "Normal",
            "eventos":         [],
            "recomendacion":   "Condiciones óptimas. Sin acción requerida.",
        }

    # El evento más grave define el nivel general
    nivel_final    = "Bajo"
    prioridad_final = "Normal"
    for evento in eventos:
        nivel, prioridad = PRIORIDADES.get(evento, ("Bajo", "Normal"))
        if nivel == "Alto":
            nivel_final = "Alto"
            prioridad_final = prioridad
            break
        elif nivel == "Medio" and nivel_final != "Alto":
            nivel_final = "Medio"
            prioridad_final = prioridad

    # Regla de municipio_cultivos: si importancia es "Alta", elevar alerta
    if importancia_municipio == "Alta" and nivel_final != "Alto":
        nivel_final     = "Alto"
        prioridad_final = "Acción Inmediata"

    return {
        "cultivo":         cultivo_nombre,
        "etapa":           etapa["etapa"],
        "porcentaje_ciclo": etapa["porcentaje"],
        "nivel_riesgo":    nivel_final,
        "prioridad":       prioridad_final,
        "eventos":         eventos,
        "clima":           desv,
        "recomendacion":   _recomendacion(eventos),
    }

def _recomendacion(eventos):
    if "Estrés Hídrico" in eventos:
        return "Riego urgente. Verificar sistema de irrigación."
    if "Aborto de Floración" in eventos:
        return "Proteger cultivo. Considerar cubierta o sombra."
    if "Riesgo de Hongo" in eventos:
        return "Aplicar fungicida preventivo. Mejorar ventilación."
    if "Asfixia Radicular" in eventos:
        return "Revisar drenaje. Evitar riego adicional."
    if "Evento Sequía" in eventos:
        return "Iniciar riego de emergencia."
    return "Monitorear condiciones en las próximas 24h."