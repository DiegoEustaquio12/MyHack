from flask import Blueprint, jsonify, render_template, request, session, url_for
from datetime import date
from .models import Cultivo, Idoneo, MunicipioCultivo, Parcela   # ← Parcela agregada
from . import db
from .services.clima import obtener_clima
from .services.prediccion import calcular_etapa, calcular_desviaciones, detectar_eventos
from .services.soluciones import generar_salida_completa
from .usuarios import USUARIOS

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


@main.route("/bitacora/<int:parcela_id>")
def bitacora(parcela_id):
    """Página de bitácora de una parcela específica del usuario."""
    if "usuario" not in session:
        return render_template("index.html")

    parcela = Parcela.query.get_or_404(parcela_id)
    # Pasamos la parcela al template; el HTML usa {{ cultivo.id }} → ahora es parcela.id
    return render_template("bitacora.html", cultivo=parcela)


# ========================
# API PARCELAS (NUEVO)
# ========================
@main.route("/api/parcelas", methods=["GET"])
def api_listar_parcelas():
    """Devuelve las parcelas del usuario en sesión."""
    if "usuario" not in session:
        return jsonify({"error": "No autenticado"}), 401

    parcelas = Parcela.query.filter_by(usuario=session["usuario"]).all()
    return jsonify([p.to_dict() for p in parcelas])


@main.route("/api/parcelas", methods=["POST"])
def api_crear_parcela():
    """
    Recibe { tipo, nombre, lugar, lat, lon } desde mapa.js
    y guarda la parcela en BD.
    Devuelve { ok, parcela_id } para que el JS pueda redirigir.
    """
    if "usuario" not in session:
        return jsonify({"error": "No autenticado"}), 401

    data   = request.get_json(silent=True) or {}
    tipo   = data.get("tipo", "").strip()
    nombre = data.get("nombre", "").strip()
    lugar  = data.get("lugar", "")
    lat    = data.get("lat")
    lon    = data.get("lon")

    if not tipo or not nombre:
        return jsonify({"ok": False, "error": "Faltan datos obligatorios"}), 400

    # Buscar el cultivo del catálogo que coincida con el tipo
    # (el tipo del select es "maiz", "chile"… y Cultivo.tipo tiene el mismo valor)
    cultivo_catalogo = Cultivo.query.filter(
        Cultivo.tipo.ilike(tipo)
    ).first()

    parcela = Parcela(
        usuario    = session["usuario"],
        nombre     = nombre,
        tipo       = tipo,
        lat        = lat,
        lon        = lon,
        lugar      = lugar,
        cultivo_id = cultivo_catalogo.id if cultivo_catalogo else None,
    )
    db.session.add(parcela)
    db.session.commit()

    return jsonify({"ok": True, "parcela_id": parcela.id})


# ========================
# API BITÁCORA
# ========================
@main.route("/api/bitacora/<int:parcela_id>", methods=["GET"])
def api_bitacora(parcela_id):
    """
    Ahora recibe un parcela_id (Parcela del usuario).
    Usa el cultivo_id de la parcela para buscar condiciones idóneas.
    """
    parcela = Parcela.query.get_or_404(parcela_id)

    if not parcela.cultivo_id:
        return jsonify({"error": "Parcela sin cultivo de catálogo asignado"}), 404

    cultivo  = Cultivo.query.get_or_404(parcela.cultivo_id)
    idoneo   = Idoneo.query.filter_by(cultivo_id=parcela.cultivo_id).first()
    municipio_cultivo = MunicipioCultivo.query.filter_by(
        cultivo_id=parcela.cultivo_id
    ).first()

    if not idoneo:
        return jsonify({"error": "Sin datos de condiciones ideales"}), 404

    # Coordenadas: primero las de la parcela, luego las del query param
    lat = parcela.lat or request.args.get("lat", 19.04, type=float)
    lon = parcela.lon or request.args.get("lon", -98.20, type=float)

    # ── 1. CLIMA ──────────────────────────────────────────────
    try:
        clima_raw    = obtener_clima(lat, lon)
        clima_actual = clima_raw.get("current", {})
        pronostico   = clima_raw.get("daily", {})
    except Exception as e:
        return jsonify({"error": f"Error al obtener clima: {str(e)}"}), 502

    # ── 2. ETAPA DEL CULTIVO ──────────────────────────────────
    try:
        fecha_siembra = date.fromisoformat(cultivo.siembra_inicio)
    except Exception:
        fecha_siembra = date.today()

    etapa = calcular_etapa(fecha_siembra, cultivo.dias_siembra_cosecha)

    # ── 3. DESVIACIONES Y EVENTOS ─────────────────────────────
    idoneo_dict = {
        "temp_max_c":       idoneo.temp_max_c,
        "temp_min_c":       idoneo.temp_min_c,
        "humedad_relativa": idoneo.humedad_relativa,
    }
    desv   = calcular_desviaciones(clima_actual, idoneo_dict)
    eventos = detectar_eventos(
        desv,
        etapa,
        temp_max_dia=pronostico.get("temperature_2m_max", [0])[0],
        temp_min_dia=pronostico.get("temperature_2m_min", [0])[0],
    )

    # ── 4. SOLUCIONES ─────────────────────────────────────────
    municipio_nombre = (
        parcela.lugar
        or (municipio_cultivo.nombre if municipio_cultivo else "Puebla")
    )
    importancia = municipio_cultivo.importancia if municipio_cultivo else "Media"

    salida = generar_salida_completa(
        municipio_nombre,
        cultivo.nombre,
        etapa,
        desv,
        eventos,
        importancia,
    )

    # ── 5. PRONÓSTICO 7 DÍAS ──────────────────────────────────
    fechas        = pronostico.get("time", [])
    pronostico_7d = []
    for i in range(7):
        pronostico_7d.append({
            "fecha":    fechas[i] if i < len(fechas) else "",
            "temp_max": pronostico.get("temperature_2m_max", [None]*7)[i],
            "temp_min": pronostico.get("temperature_2m_min", [None]*7)[i],
            "lluvia":   pronostico.get("precipitation_sum",  [None]*7)[i],
        })

    return jsonify({
        "cultivo": {
            "id":     parcela.id,
            "nombre": parcela.nombre,          # nombre de la parcela del usuario
            "tipo":   cultivo.tipo,
            "etapa":  etapa,
        },
        "clima_actual": {
            "temp":    desv.get("temp"),
            "humedad": desv.get("humedad"),
            "lluvia":  desv.get("lluvia"),
        },
        "diagnostico":  salida.get("diagnostico"),
        "nivel_riesgo": salida.get("nivel_riesgo"),
        "color":        salida.get("color"),
        "urgencia":     salida.get("urgencia"),
        "puntaje":      salida.get("puntaje"),
        "eventos":      salida.get("eventos"),
        "soluciones":   salida.get("soluciones"),
        "pronostico_7d": pronostico_7d,
    })


# ========================
# LOGIN
# ========================
@main.route("/login", methods=["POST"])
def login():
    data     = request.get_json(silent=True) or {}
    usuario  = data.get("usuario", "").strip()
    password = data.get("contrasena", "").strip()

    if USUARIOS.get(usuario) == password:
        session["usuario"] = usuario
        return jsonify({"ok": True, "redirect": url_for("main.dashboard")})

    return jsonify({"ok": False, "error": "Usuario o contraseña incorrectos"}), 401


# ========================
# REGISTRO
# ========================
@main.route("/registrar", methods=["POST"])
def registrar():
    data     = request.get_json(silent=True) or {}
    nombre   = data.get("nombre",    "").strip()
    usuario  = data.get("usuario",   "").strip()
    password = data.get("contrasena","").strip()

    if not usuario or not password or not nombre:
        return jsonify({"ok": False, "error": "Faltan datos obligatorios"}), 400

    if usuario in USUARIOS:
        return jsonify({"ok": False, "error": "Este correo ya está registrado"}), 400

    USUARIOS[usuario] = password
    return jsonify({"ok": True})


# ========================
# LOGOUT
# ========================
@main.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")