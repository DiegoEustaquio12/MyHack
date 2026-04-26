from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session
from .models import Cultivo, Idoneo, MunicipioCultivo

# Importación del diccionario de usuarios desde el nuevo archivo
from .usuarios import USUARIOS

# ── Servicios de predicción (algoritmos del proyecto) ──
from .services.prediccion import calcular_etapa, calcular_desviaciones, detectar_eventos
from .services.soluciones import generar_salida_completa

import random
from datetime import date

main = Blueprint("main", __name__)


# ══════════════════════════════════════════════════════════════
# DATOS DE PRUEBA
# ══════════════════════════════════════════════════════════════

# Cultivo genérico que simula un registro de la BD
CULTIVO_PRUEBA = {
    "id":                     1,
    "nombre":                 "Maíz",
    "parcela":                "Parcela Norte",
    "municipio":              "Tehuacán",
    "tipo":                   "Grano",
    "siembra_inicio":         date(2025, 3, 15),
    "dias_siembra_cosecha":   150,
    "importancia":            "Alta",
    "icono":                  "🌽",
    "idoneo": {
        "temp_min_c":        10.0,
        "temp_optima_c":     24.0,
        "temp_max_c":        35.0,
        "humedad_relativa":  60.0,
        "ph_min":            5.5,
        "ph_max":            7.0,
        "riego_frecuencia":  "cada 7 días",
    },
}


# ══════════════════════════════════════════════════════════════
# RUTA ORIGINAL
# ══════════════════════════════════════════════════════════════

@main.route("/")
def inicio():
    return render_template("index.html")


# ══════════════════════════════════════════════════════════════
# AUTENTICACIÓN
# ══════════════════════════════════════════════════════════════

@main.route("/login", methods=["POST"])
def login():
    """Valida contra el diccionario importado de usuarios.py."""
    data     = request.get_json(silent=True) or {}
    usuario  = data.get("usuario", "").strip()
    password = data.get("contrasena", "").strip()

    # Validación utilizando el diccionario importado
    if USUARIOS.get(usuario) == password:
        session["usuario"] = usuario
        # Se devuelve la instrucción de redirección al front-end
        return jsonify({"ok": True, "redirect": url_for("main.dashboard")})

    return jsonify({"ok": False, "error": "Usuario o contraseña incorrectos"}), 401


@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.inicio"))


# ══════════════════════════════════════════════════════════════
# VISTAS PROTEGIDAS
# ══════════════════════════════════════════════════════════════

@main.route("/dashboard")
def dashboard():
    """Dashboard de cultivos — requiere sesión activa."""
    if "usuario" not in session:
        return redirect(url_for("main.inicio"))
    return render_template("dashboard.html", usuario=session["usuario"])


@main.route("/bitacora")
def bitacora():
    """Bitácora del cultivo de prueba."""
    if "usuario" not in session:
        return redirect(url_for("main.inicio"))
    return render_template("bitacora.html", cultivo=CULTIVO_PRUEBA)


@main.route("/recomendaciones/<int:cultivo_id>")
def recomendaciones(cultivo_id):
    """
    Genera recomendaciones combinando datos de prueba, clima y algoritmos.
    """
    if "usuario" not in session:
        return redirect(url_for("main.inicio"))

    # ── Clima de prueba ──
    temp_base = round(28 + random.uniform(-4, 10), 1)
    clima_actual = {
        "temperature_2m":       temp_base,
        "relative_humidity_2m": int(32 + random.uniform(-5, 25)),
        "precipitation":        round(random.uniform(0, 2), 1),
        "wind_speed_10m":       round(random.uniform(5, 18), 1),
    }
    temp_max_dia = round(temp_base + random.uniform(3, 9),  1)
    temp_min_dia = round(temp_base - random.uniform(8, 16), 1)

    # ── Algoritmos del proyecto ──
    etapa   = calcular_etapa(CULTIVO_PRUEBA["siembra_inicio"],
                             CULTIVO_PRUEBA["dias_siembra_cosecha"])
    desv    = calcular_desviaciones(clima_actual, CULTIVO_PRUEBA["idoneo"])
    eventos = detectar_eventos(desv, etapa, temp_max_dia, temp_min_dia)

    resultado = generar_salida_completa(
        municipio            = CULTIVO_PRUEBA["municipio"],
        cultivo_nombre       = CULTIVO_PRUEBA["nombre"],
        etapa                = etapa,
        desv                 = desv,
        eventos              = eventos,
        importancia_municipio= CULTIVO_PRUEBA["importancia"],
    )

    resultado["clima_actual"] = clima_actual
    resultado["temp_max_dia"] = temp_max_dia
    resultado["temp_min_dia"] = temp_min_dia

    return render_template("principal.html", resultado=resultado, cultivo=CULTIVO_PRUEBA)