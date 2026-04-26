"""
seed.py — Poblar la BD con el catálogo base de cultivos e idóneos.

Uso:
    flask shell
    >>> exec(open('seed.py').read())

O directamente:
    python seed.py
"""

from app import create_app, db
from app.models import Cultivo, Idoneo

app = create_app()

CULTIVOS = [
    {
        "nombre": "Maíz",
        "tipo":   "maiz",
        "siembra_inicio":       "2025-04-15",
        "cosecha_fin":          "2025-10-30",
        "dias_siembra_cosecha": 180,
        "idoneo": {
            "temp_min_c":       10.0,
            "temp_optima_c":    25.0,
            "temp_max_c":       35.0,
            "riego_frecuencia": "Cada 8 días",
            "ph_min":           5.5,
            "ph_max":           7.0,
            "humedad_relativa": 60.0,
        }
    },
    {
        "nombre": "Chile Poblano",
        "tipo":   "chile",
        "siembra_inicio":       "2025-03-01",
        "cosecha_fin":          "2025-08-31",
        "dias_siembra_cosecha": 180,
        "idoneo": {
            "temp_min_c":       15.0,
            "temp_optima_c":    24.0,
            "temp_max_c":       32.0,
            "riego_frecuencia": "Cada 5 días",
            "ph_min":           6.0,
            "ph_max":           7.0,
            "humedad_relativa": 65.0,
        }
    },
    {
        "nombre": "Frijol",
        "tipo":   "frijol",
        "siembra_inicio":       "2025-06-01",
        "cosecha_fin":          "2025-10-15",
        "dias_siembra_cosecha": 120,
        "idoneo": {
            "temp_min_c":       10.0,
            "temp_optima_c":    22.0,
            "temp_max_c":       30.0,
            "riego_frecuencia": "Cada 10 días",
            "ph_min":           6.0,
            "ph_max":           7.5,
            "humedad_relativa": 55.0,
        }
    },
    {
        "nombre": "Aguacate",
        "tipo":   "aguacate",
        "siembra_inicio":       "2025-01-01",
        "cosecha_fin":          "2025-12-31",
        "dias_siembra_cosecha": 365,
        "idoneo": {
            "temp_min_c":       5.0,
            "temp_optima_c":    20.0,
            "temp_max_c":       30.0,
            "riego_frecuencia": "Cada 15 días",
            "ph_min":           5.0,
            "ph_max":           7.0,
            "humedad_relativa": 60.0,
        }
    },
    {
        "nombre": "Nopal",
        "tipo":   "nopal",
        "siembra_inicio":       "2025-02-01",
        "cosecha_fin":          "2025-11-30",
        "dias_siembra_cosecha": 270,
        "idoneo": {
            "temp_min_c":       8.0,
            "temp_optima_c":    25.0,
            "temp_max_c":       38.0,
            "riego_frecuencia": "Cada 20 días",
            "ph_min":           6.0,
            "ph_max":           8.0,
            "humedad_relativa": 40.0,
        }
    },
    {
        "nombre": "Amaranto",
        "tipo":   "amaranto",
        "siembra_inicio":       "2025-05-01",
        "cosecha_fin":          "2025-10-01",
        "dias_siembra_cosecha": 150,
        "idoneo": {
            "temp_min_c":       10.0,
            "temp_optima_c":    28.0,
            "temp_max_c":       36.0,
            "riego_frecuencia": "Cada 12 días",
            "ph_min":           6.0,
            "ph_max":           7.5,
            "humedad_relativa": 50.0,
        }
    },
    {
        "nombre": "Jitomate",
        "tipo":   "jitomate",
        "siembra_inicio":       "2025-02-15",
        "cosecha_fin":          "2025-07-31",
        "dias_siembra_cosecha": 165,
        "idoneo": {
            "temp_min_c":       13.0,
            "temp_optima_c":    23.0,
            "temp_max_c":       30.0,
            "riego_frecuencia": "Cada 4 días",
            "ph_min":           5.5,
            "ph_max":           6.8,
            "humedad_relativa": 65.0,
        }
    },
    {
        "nombre": "Papa",
        "tipo":   "papa",
        "siembra_inicio":       "2025-03-01",
        "cosecha_fin":          "2025-08-15",
        "dias_siembra_cosecha": 165,
        "idoneo": {
            "temp_min_c":       7.0,
            "temp_optima_c":    18.0,
            "temp_max_c":       25.0,
            "riego_frecuencia": "Cada 7 días",
            "ph_min":           4.8,
            "ph_max":           6.5,
            "humedad_relativa": 70.0,
        }
    },
]

with app.app_context():
    insertados = 0
    for data in CULTIVOS:
        # Evitar duplicados si se corre el seed más de una vez
        existe = Cultivo.query.filter_by(tipo=data["tipo"]).first()
        if existe:
            print(f"  [SKIP] {data['nombre']} ya existe.")
            continue

        cultivo = Cultivo(
            nombre                = data["nombre"],
            tipo                  = data["tipo"],
            siembra_inicio        = data["siembra_inicio"],
            cosecha_fin           = data["cosecha_fin"],
            dias_siembra_cosecha  = data["dias_siembra_cosecha"],
        )
        db.session.add(cultivo)
        db.session.flush()   # obtener cultivo.id antes del commit

        idata  = data["idoneo"]
        idoneo = Idoneo(
            cultivo_id       = cultivo.id,
            temp_min_c       = idata["temp_min_c"],
            temp_optima_c    = idata["temp_optima_c"],
            temp_max_c       = idata["temp_max_c"],
            riego_frecuencia = idata["riego_frecuencia"],
            ph_min           = idata["ph_min"],
            ph_max           = idata["ph_max"],
            humedad_relativa = idata["humedad_relativa"],
        )
        db.session.add(idoneo)
        insertados += 1
        print(f"  [OK]   {data['nombre']}")

    db.session.commit()
    print(f"\n✅ Seed completado: {insertados} cultivos insertados.")