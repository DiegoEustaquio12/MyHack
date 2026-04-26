SOLUCIONES = {
    "Estrés Hídrico": {
        "accion":  "Riego urgente en las próximas 6 horas.",
        "detalle": "Aplicar 50-80 mm de lámina de riego. Priorizar horas de menor calor (5-8am).",
        "insumos": "Sistema de riego, agua disponible.",
    },
    "Aborto de Floración": {
        "accion":  "Proteger la flor del estrés térmico.",
        "detalle": "Instalar malla sombra al 30-50%. Si hay helada, usar cubierta flotante nocturna.",
        "insumos": "Malla sombra, cubierta agrícola, termómetro de campo.",
    },
    "Riesgo de Hongo": {
        "accion":  "Aplicar fungicida preventivo hoy.",
        "detalle": "Usar fungicida cúprico o azufre mojable. Mejorar ventilación entre plantas.",
        "insumos": "Fungicida (cobre o azufre), bomba aspersora.",
    },
    "Asfixia Radicular": {
        "accion":  "Detener riego y revisar drenaje inmediatamente.",
        "detalle": "Abrir surcos de drenaje. No aplicar más agua hasta que el suelo drene.",
        "insumos": "Azadón, canales de drenaje.",
    },
    "Cosecha en Riesgo": {
        "accion":  "Adelantar cosecha si el cultivo supera el 75% del ciclo.",
        "detalle": "Evaluar madurez fisiológica. Cosechar antes de que el evento climático dañe el grano.",
        "insumos": "Equipo de cosecha, almacén disponible.",
    },
    "Evento Calor": {
        "accion":  "Monitorear temperatura cada 4 horas.",
        "detalle": "Riego ligero en follaje si supera 40°C. Evitar labores en horas de máximo calor.",
        "insumos": "Termómetro, sistema de riego.",
    },
    "Evento Frío": {
        "accion":  "Preparar protección nocturna.",
        "detalle": "Cubrir cultivo al atardecer. Considerar riego antes de helada para proteger raíces.",
        "insumos": "Cubierta flotante, termómetro mínimo.",
    },
    "Evento Sequía": {
        "accion":  "Iniciar riego de emergencia.",
        "detalle": "Aplicar riego por goteo o aspersión. Revisar humedad a 20 cm de profundidad.",
        "insumos": "Sistema de riego, tensiómetro de suelo.",
    },
    "Retraso de Ciclo": {
        "accion":  "Ajustar calendario agrícola.",
        "detalle": "Documentar retraso. Considerar fertilización nitrogenada para acelerar recuperación.",
        "insumos": "Fertilizante nitrogenado, bitácora de campo.",
    },
}

# Niveles de urgencia según puntaje
URGENCIA = {
    "Alto":  "Acción Inmediata (24h)",
    "Medio": "Preparación (48-72h)",
    "Bajo":  "Monitoreo Preventivo",
}

COLORES = {
    "Alto":  "rojo",
    "Medio": "amarillo",
    "Bajo":  "verde",
}


def calcular_puntaje(delta_t: float, etapa: str, eventos: list, importancia_municipio: str) -> int:
    puntaje = 0

    if delta_t > 5:
        puntaje += 3
    if etapa == "Floración":
        puntaje += 2
    if len(eventos) > 0:
        puntaje += 4
    if importancia_municipio == "Alta":
        puntaje += 2

    return puntaje


def clasificar_riesgo(puntaje: int) -> str:
    if puntaje >= 8:
        return "Alto"
    elif puntaje >= 5:
        return "Medio"
    else:
        return "Bajo"


def construir_diagnostico(municipio: str, eventos: list, delta_t: float, etapa: str) -> str:
    """
    Generador basico de texto UX del diagnóstico.
    """
    evento_principal = eventos[0] if eventos else "condiciones normales"
    return (
        f"En el municipio de {municipio}, su cultivo presenta '{evento_principal}' "
        f"con una desviación de {abs(delta_t):.1f}°C durante la etapa de {etapa}."
    )


def obtener_soluciones(eventos: list) -> list:
    """
    Multiples eventos con el diccionario de soluciones.
    """
    resultado = []
    for evento in eventos:
        if evento in SOLUCIONES:
            resultado.append({
                "evento":  evento,
                **SOLUCIONES[evento],
            })
    return resultado


def generar_salida_completa(
    municipio: str,
    cultivo_nombre: str,
    etapa: dict,
    desv: dict,
    eventos: list,
    importancia_municipio: str,
) -> dict:
    """
    Función principal
    """
    delta_t = desv["delta_calor"]

    puntaje       = calcular_puntaje(delta_t, etapa["etapa"], eventos, importancia_municipio)
    nivel_riesgo  = clasificar_riesgo(puntaje)
    urgencia = URGENCIA[nivel_riesgo]
    color    = COLORES[nivel_riesgo]
    diagnostico = construir_diagnostico(municipio, eventos, delta_t, etapa["etapa"])
    soluciones = obtener_soluciones(eventos)

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