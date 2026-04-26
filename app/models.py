from . import db


class Cultivo(db.Model):
    __tablename__ = "cultivos"

    id                      = db.Column(db.Integer, primary_key=True)
    nombre                  = db.Column(db.String(100), nullable=False)
    tipo                    = db.Column(db.String(50))
    siembra_inicio          = db.Column(db.String(20))
    cosecha_fin             = db.Column(db.String(20))
    dias_siembra_cosecha    = db.Column(db.Integer)
    municipios_clave_puebla = db.Column(db.Text)

    condiciones = db.relationship("Idoneo", backref="cultivo", uselist=False, lazy=True)

    def to_dict(self):
        return {
            "id":                   self.id,
            "nombre":               self.nombre,
            "tipo":                 self.tipo,
            "siembra_inicio":       self.siembra_inicio,
            "cosecha_fin":          self.cosecha_fin,
            "dias_siembra_cosecha": self.dias_siembra_cosecha,
            "municipios":           self.municipios_clave_puebla,
        }


class Idoneo(db.Model):
    __tablename__ = "idoneo"

    id               = db.Column(db.Integer, primary_key=True)
    cultivo_id       = db.Column(db.Integer, db.ForeignKey("cultivos.id"), nullable=False)
    temp_min_c       = db.Column(db.Float)
    temp_optima_c    = db.Column(db.Float)
    temp_max_c       = db.Column(db.Float)
    riego_frecuencia = db.Column(db.String(50))
    ph_min           = db.Column(db.Float)
    ph_max           = db.Column(db.Float)
    humedad_relativa = db.Column(db.Float)

    def to_dict(self):
        return {
            "temp_min_c":       self.temp_min_c,
            "temp_optima_c":    self.temp_optima_c,
            "temp_max_c":       self.temp_max_c,
            "riego_frecuencia": self.riego_frecuencia,
            "ph_min":           self.ph_min,
            "ph_max":           self.ph_max,
            "humedad_relativa": self.humedad_relativa,
        }


class MunicipioCultivo(db.Model):
    __tablename__ = "municipio_cultivos"

    id          = db.Column(db.Integer, primary_key=True)
    nombre      = db.Column(db.String(100))
    cultivo_id  = db.Column(db.Integer, db.ForeignKey("cultivos.id"))
    importancia = db.Column(db.String(20))


# ── NUEVA TABLA ───────────────────────────────────────────────────────────────
class Parcela(db.Model):
    """
    Parcela registrada por el usuario en el dashboard.
    Apunta al catálogo de cultivos (Cultivo) para obtener
    condiciones idóneas, días de ciclo, etc.
    """
    __tablename__ = "parcelas"

    id         = db.Column(db.Integer, primary_key=True)
    usuario    = db.Column(db.String(100), nullable=False)          # session["usuario"]
    nombre     = db.Column(db.String(100), nullable=False)          # "Parcela Norte"
    tipo       = db.Column(db.String(50),  nullable=False)          # "maiz", "chile"…
    lat        = db.Column(db.Float)
    lon        = db.Column(db.Float)
    lugar      = db.Column(db.String(200))                          # nombre del municipio
    cultivo_id = db.Column(db.Integer, db.ForeignKey("cultivos.id"))# catálogo

    cultivo_ref = db.relationship("Cultivo", foreign_keys=[cultivo_id])

    def to_dict(self):
        return {
            "id":         self.id,
            "nombre":     self.nombre,
            "tipo":       self.tipo,
            "lat":        self.lat,
            "lon":        self.lon,
            "lugar":      self.lugar,
            "cultivo_id": self.cultivo_id,
        }