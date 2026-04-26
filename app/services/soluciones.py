# app/services/soluciones.py

SOLUCIONES = {

    # ── Eventos simples (una variable) ────────────────────────
    "Evento Calor": {
        "diagnostico": "Temperatura por encima del límite de seguridad del cultivo.",
        "fisiologia":  "La planta eleva su temperatura basal al cerrar estomas para conservar agua, deteniendo la fotosíntesis.",
        "acciones": [
            "Aplicar riegos de auxilio para reducir la temperatura del suelo por evaporación.",
            "Evitar labores agrícolas en horas de máximo calor (12:00–16:00).",
        ],
        "referencia": "FAO – Manejo del estrés hídrico en cultivos básicos.",
        "urgencia_base": "Normal",
    },

    "Evento Frío": {
        "diagnostico": "Temperatura por debajo del mínimo biológico del cultivo.",
        "fisiologia":  "Las enzimas metabólicas pierden actividad; el agua intracelular puede congelarse y romper membranas.",
        "acciones": [
            "Aplicar fertilización foliar rica en Potasio para fortalecer las paredes celulares contra el frío.",
            "Cubrir el cultivo al atardecer con cubierta flotante si se esperan heladas nocturnas.",
        ],
        "referencia": "INIFAP – Guía de manejo de heladas en valles de Puebla.",
        "urgencia_base": "Normal",
    },

    "Déficit de Humedad": {
        "diagnostico": "El aire está más seco de lo ideal para la transpiración del cultivo.",
        "fisiologia":  "La demanda evaporativa supera la capacidad de absorción radicular.",
        "acciones": [
            "Aumentar la frecuencia de riego y considerar el uso de acolchado orgánico para retener humedad.",
            "Revisar humedad del suelo a 20 cm de profundidad con tensiómetro.",
        ],
        "referencia": "FAO – Manejo del estrés hídrico en cultivos básicos.",
        "urgencia_base": "Normal",
    },

    "Exceso de Humedad": {
        "diagnostico": "Humedad ambiental saturada; riesgo de falta de transpiración.",
        "fisiologia":  "El exceso de vapor reduce el gradiente de presión que permite que la planta transpire y absorba nutrientes.",
        "acciones": [
            "Suspender riegos programados.",
            "Despejar malezas para mejorar la circulación de aire entre plantas.",
        ],
        "referencia": "INIFAP – Guía técnica para el manejo de enfermedades foliares.",
        "urgencia_base": "Normal",
    },

    "Evento Sequía": {
        "diagnostico": "Sin precipitación y humedad crítica; riesgo de daño permanente en raíces.",
        "fisiologia":  "La planta prioriza la supervivencia cerrando estomas, lo que colapsa la producción de biomasa.",
        "acciones": [
            "Iniciar riego de emergencia inmediatamente.",
            "Aplicar acolchado orgánico (mulching) en la base para reducir temperatura del suelo hasta 4°C.",
            "Reducir o suspender fertilización nitrogenada: el nitrógeno demanda agua que la planta no tiene.",
        ],
        "referencia": "FAO – Manejo del estrés hídrico en cultivos básicos.",
        "urgencia_base": "Alta",
    },

    # ── Eventos combinados (alta prioridad) ───────────────────
    "Estrés Hídrico": {
        "diagnostico": (
            "Cierre estomático detectado: la planta está perdiendo agua más rápido "
            "de lo que sus raíces pueden absorberla (Evapotranspiración crítica)."
        ),
        "fisiologia": (
            "Al cerrar sus estomas para no perder agua, la planta detiene la fotosíntesis "
            "y su enfriamiento interno, elevando su temperatura basal."
        ),
        "acciones": [
            "Riego de auxilio nocturno: aplicar entre las 20:00 y las 04:00 h para maximizar absorción sin evaporación.",
            "Mulching (acolchado): cubrir la base con residuos de cosecha anterior para reducir temperatura del suelo hasta 4°C.",
            "Reducir fertilización nitrogenada: el nitrógeno estimula crecimiento foliar que demandará más agua.",
            "Evitar cualquier fertilización química en este momento; podría quemar raíces estresadas.",
        ],
        "referencia": "FAO – Manejo del estrés hídrico en cultivos básicos.",
        "urgencia_base": "Urgente",
    },

    "Riesgo de Hongo": {
        "diagnostico": (
            "Ambiente de incubadora detectado: condiciones óptimas para germinación "
            "de esporas de Roya o Mildiu."
        ),
        "fisiologia": (
            "La combinación de temperatura alta con humedad superior al óptimo por más de 12 h "
            "crea una película de agua en hojas, ideal para hongos."
        ),
        "acciones": [
            "Poda de aireación: eliminar hojas del tercio inferior del tallo para que el viento seque el exceso de humedad.",
            "Aplicar fungicidas preventivos: sales de cobre o soluciones biológicas (Bacillus subtilis).",
            "Controlar densidad de siembra: evitar microclimas estancados entre plantas.",
            "Suspender riegos por aspersión temporalmente; preferir riego por goteo.",
        ],
        "referencia": "INIFAP – Guía técnica para manejo de enfermedades foliares en granos y hortalizas (Puebla).",
        "urgencia_base": "Alta",
    },

    "Aborto de Floración": {
        "diagnostico": (
            "Alerta roja: el calor extremo está deshidratando el polen. "
            "Riesgo alto de pérdida de rendimiento (mazorcas o frutos vacíos)."
        ),
        "fisiologia": (
            "Las temperaturas superiores al máximo secan los estigmas del maíz, "
            "impidiendo la fecundación y formación de granos."
        ),
        "acciones": [
            "Bioestimulantes de emergencia: aplicar aminoácidos o extractos de algas para sintetizar proteínas de choque térmico.",
            "Riego por aspersión: actúa como climatizador artificial para bajar la temperatura alrededor de la flor.",
            "Priorización de riego: si el agua es escasa, redirigir el 100% a parcelas en etapa de floración (51–80% del ciclo).",
            "Aplicación foliar de bioestimulantes y asegurar microclima húmedo en horas de calor máximo.",
        ],
        "referencia": "CIMMYT – Efectos del estrés térmico en la reproducción de cereales.",
        "urgencia_base": "Urgente",
    },

    "Asfixia Radicular": {
        "diagnostico": (
            "El suelo se ha quedado sin poros de oxígeno; las raíces están comenzando "
            "a morir por anoxia."
        ),
        "fisiologia": (
            "Los poros del suelo se llenan de agua desplazando el oxígeno. "
            "Las raíces producen etanol, atrayendo bacterias que pudren la planta."
        ),
        "acciones": [
            "Apertura inmediata de canales de drenaje y limpieza de desagües.",
            "No pisar el terreno húmedo para evitar la compactación del suelo.",
            "Post-tratamiento: una vez que baje el agua, aplicar fertilizantes foliares (las raíces estarán débiles para absorber del suelo).",
            "Recomendación futura: usar camas elevadas de siembra para evitar encharcamientos.",
        ],
        "referencia": "SIAP – Manual de contingencias climatológicas para el sector agropecuario.",
        "urgencia_base": "Alta",
    },

    "Cosecha en Riesgo": {
        "diagnostico": "El cultivo en etapa avanzada enfrenta temperatura extrema; riesgo de pérdida de rendimiento.",
        "fisiologia":  "El estrés térmico en maduración reduce el llenado de grano y puede forzar madurez prematura.",
        "acciones": [
            "Evaluar madurez fisiológica; adelantar cosecha si el cultivo supera el 75% del ciclo.",
            "Asegurar almacén disponible antes de cosechar.",
            "Riego ligero de apoyo si el suelo está seco para no acelerar la deshidratación del grano.",
        ],
        "referencia": "CIMMYT – Efectos del estrés térmico en la reproducción de cereales.",
        "urgencia_base": "Alta",
    },

    "Choque Térmico": {
        "diagnostico": "Oscilación térmica extrema en menos de 24h detectada.",
        "fisiologia": (
            "La planta no puede ajustar sus procesos enzimáticos a cambios bruscos de temperatura; "
            "produce descontrol metabólico (común en los valles de Puebla)."
        ),
        "acciones": [
            "Mantener el suelo con humedad constante: el agua actúa como batería térmica regulando la temperatura de la raíz.",
            "Evitar riegos en las horas más frías de la noche si hay riesgo de helada.",
            "Aplicar fertilización foliar para compensar la reducción de absorción radicular.",
        ],
        "referencia": "INIFAP – Guía de manejo climático en valles altos de Puebla.",
        "urgencia_base": "Alta",
    },

    "Retraso de Ciclo": {
        "diagnostico": "Las bajas temperaturas están enlenteciendo el desarrollo fenológico del cultivo.",
        "fisiologia":  "Las reacciones enzimáticas del metabolismo vegetal se ralentizan bajo el umbral mínimo térmico.",
        "acciones": [
            "Ajustar el calendario agrícola y documentar el retraso.",
            "Considerar fertilización nitrogenada moderada para acelerar recuperación cuando el clima mejore.",
            "Revisar fechas de cosecha estimadas.",
        ],
        "referencia": "INIFAP – Guía de fenología de cultivos en Puebla.",
        "urgencia_base": "Media",
    },
}

# ── Tabla de puntaje por urgencia ─────────────────────────────
PESO_URGENCIA = {
    "Urgente": 4,
    "Alta":    3,
    "Media":   2,
    "Normal":  1,
}

URGENCIA_POR_NIVEL = {
    "Alto":  "Acción Inmediata (24h)",
    "Medio": "Preparación (48–72h)",
    "Bajo":  "Monitoreo Preventivo",
}

COLORES = {
    "Alto":  "rojo",
    "Medio": "amarillo",
    "Bajo":  "verde",
}


def calcular_puntaje(delta_t: float, etapa: str,
                     eventos: list, importancia_municipio: str) -> int:
    puntaje = 0

    if delta_t > 5:
        puntaje += 3
    if etapa == "Floración":
        puntaje += 2
    if len(eventos) > 0:
        puntaje += 4
    if importancia_municipio == "Alta":
        puntaje += 2

    # Bonus por eventos de máxima prioridad
    eventos_urgentes = {"Estrés Hídrico", "Aborto de Floración", "Choque Térmico"}
    if any(e in eventos_urgentes for e in eventos):
        puntaje += 2

    return puntaje


def clasificar_riesgo(puntaje: int) -> str:
    if puntaje >= 8:
        return "Alto"
    elif puntaje >= 5:
        return "Medio"
    return "Bajo"


def construir_diagnostico(municipio: str, eventos: list,
                           delta_t: float, etapa: str) -> str:
    if not eventos:
        return (
            f"En el municipio de {municipio}, el cultivo presenta condiciones "
            f"dentro de los rangos óptimos durante la etapa de {etapa}."
        )
    evento_principal = eventos[0]
    diag = SOLUCIONES.get(evento_principal, {}).get("diagnostico", "")
    return (
        f"En el municipio de {municipio}, su cultivo presenta '{evento_principal}' "
        f"con una desviación de {abs(delta_t):.1f}°C durante la etapa de {etapa}. "
        f"{diag}"
    )


def obtener_soluciones(eventos: list) -> list:
    """Cruza eventos con el diccionario; ordena por urgencia descendente."""
    resultado = []
    for evento in eventos:
        if evento in SOLUCIONES:
            s = SOLUCIONES[evento]
            resultado.append({
                "evento":      evento,
                "diagnostico": s["diagnostico"],
                "fisiologia":  s["fisiologia"],
                "acciones":    s["acciones"],
                "referencia":  s["referencia"],
                "urgencia":    s["urgencia_base"],
                "peso":        PESO_URGENCIA.get(s["urgencia_base"], 1),
            })

    resultado.sort(key=lambda x: x["peso"], reverse=True)
    return resultado


def generar_salida_completa(
    municipio: str,
    cultivo_nombre: str,
    etapa: dict,
    desv: dict,
    eventos: list,
    importancia_municipio: str,
) -> dict:

    delta_t = desv["delta_calor"]

    puntaje      = calcular_puntaje(delta_t, etapa["etapa"], eventos, importancia_municipio)
    nivel_riesgo = clasificar_riesgo(puntaje)
    urgencia     = URGENCIA_POR_NIVEL[nivel_riesgo]
    color        = COLORES[nivel_riesgo]
    diagnostico  = construir_diagnostico(municipio, eventos, delta_t, etapa["etapa"])
    soluciones   = obtener_soluciones(eventos)

    return {
        "municipio":    municipio,
        "cultivo":      cultivo_nombre,
        "etapa":        etapa["etapa"],
        "porcentaje":   etapa["porcentaje"],
        "puntaje":      puntaje,
        "nivel_riesgo": nivel_riesgo,
        "color":        color,
        "urgencia":     urgencia,
        "diagnostico":  diagnostico,
        "eventos":      eventos,
        "soluciones":   soluciones,
        "clima":        desv,
    }