from flask import Blueprint, jsonify, render_template, request, session, url_for
from datetime import date
from .models import Cultivo, Idoneo, MunicipioCultivo
from . import db
from .services.clima import obtener_clima
from .services.prediccion import calcular_etapa, calcular_desviaciones, detectar_eventos
from .services.soluciones import generar_salida_completa
from .usuarios import USUARIOS  # <-- Asegúrate de tener este archivo

main = Blueprint("main", __name__)


# ========================
# VISTAS
# ========================
@main.route("/")
def inicio():
    return render_template("index.html")


@main.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return render_template("index.html")
    return render_template("dashboard.html")


@main.route("/bitacora/<int:cultivo_id>")
def bitacora(cultivo_id):
    """Página de bitácora de un cultivo específico."""
    if "usuario" not in session:
        return render_template("index.html")

    cultivo = Cultivo.query.get_or_404(cultivo_id)
    return render_template("bitacora.html", cultivo=cultivo)


# ========================
# API BITÁCORA
# ========================
@main.route("/api/bitacora/<int:cultivo_id>", methods=["GET"])
def api_bitacora(cultivo_id):
    cultivo = Cultivo.query.get_or_404(cultivo_id)
    idoneo = Idoneo.query.filter_by(cultivo_id=cultivo_id).first()
    municipio_cultivo = MunicipioCultivo.query.filter_by(
        cultivo_id=cultivo_id
    ).first()

    if not idoneo:
        return jsonify({"error": "Sin datos de condiciones ideales"}), 404

    # Coordenadas (pueden venir del frontend)
    lat = request.args.get("lat", 19.04, type=float)
    lon = request.args.get("lon", -98.20, type=float)

    # ========================
    # 1. CLIMA
    # ========================
    try:
        clima_raw = obtener_clima(lat, lon)
        clima_actual = clima_raw.get("current", {})
        pronostico = clima_raw.get("daily", {})
    except Exception as e:
        return jsonify({"error": f"Error al obtener clima: {str(e)}"}), 502

    # ========================
    # 2. ETAPA DEL CULTIVO
    # ========================
    try:
        fecha_siembra = date.fromisoformat(cultivo.siembra_inicio)
    except Exception:
        fecha_siembra = date.today()

    etapa = calcular_etapa(fecha_siembra, cultivo.dias_siembra_cosecha)

    # ========================
    # 3. DESVIACIONES Y EVENTOS
    # ========================
    idoneo_dict = {
        "temp_max_c": idoneo.temp_max_c,
        "temp_min_c": idoneo.temp_min_c,
        "humedad_relativa": idoneo.humedad_relativa,
    }

    desv = calcular_desviaciones(clima_actual, idoneo_dict)

    eventos = detectar_eventos(
        desv,
        etapa,
        temp_max_dia=pronostico.get("temperature_2m_max", [0])[0],
        temp_min_dia=pronostico.get("temperature_2m_min", [0])[0],
    )

    # ========================
    # 4. SOLUCIONES
    # ========================
    municipio_nombre = municipio_cultivo.nombre if municipio_cultivo else "Puebla"
    importancia = municipio_cultivo.importancia if municipio_cultivo else "Media"

    salida = generar_salida_completa(
        municipio_nombre,
        cultivo.nombre,
        etapa,
        desv,
        eventos,
        importancia,
    )

    # ========================
    # 5. PRONÓSTICO 7 DÍAS
    # ========================
    pronostico_7d = []
    fechas = pronostico.get("time", [])

    for i in range(7):
        pronostico_7d.append({
            "fecha": fechas[i] if i < len(fechas) else "",
            "temp_max": pronostico.get("temperature_2m_max", [None]*7)[i],
            "temp_min": pronostico.get("temperature_2m_min", [None]*7)[i],
            "lluvia": pronostico.get("precipitation_sum", [None]*7)[i],
        })

    return jsonify({
        "cultivo": {
            "id": cultivo.id,
            "nombre": cultivo.nombre,
            "tipo": cultivo.tipo,
            "etapa": etapa,
        },
        "clima_actual": {
            "temp": desv.get("temp"),
            "humedad": desv.get("humedad"),
            "lluvia": desv.get("lluvia"),
        },
        "diagnostico": salida.get("diagnostico"),
        "nivel_riesgo": salida.get("nivel_riesgo"),
        "color": salida.get("color"),
        "urgencia": salida.get("urgencia"),
        "puntaje": salida.get("puntaje"),
        "eventos": salida.get("eventos"),
        "soluciones": salida.get("soluciones"),
        "pronostico_7d": pronostico_7d,
    })


# ========================
# LOGIN
# ========================
@main.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    usuario = data.get("usuario", "").strip()
    password = data.get("contrasena", "").strip()

    if USUARIOS.get(usuario) == password:
        session["usuario"] = usuario
        return jsonify({
            "ok": True,
            "redirect": url_for("main.dashboard")
        })

    return jsonify({
        "ok": False,
        "error": "Usuario o contraseña incorrectos"
    }), 401


# ========================
# LOGOUT
# ========================
@main.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")