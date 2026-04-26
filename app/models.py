from . import db

#Tabla Municipios
class Municipio(db.Model):
    __tablename__ = "municipios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cultivos = db.relationship("Cultivo", backref="municipio", lazy=True)

# Tabla Cultivos
class Cultivo(db.Model):
    __tablename__ = "cultivos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    temperatura_optima = db.Column(db.Float)
    humedad_optima = db.Column(db.Float)
    tipo_suelo = db.Column(db.String(50))
    ciclo_dias = db.Column(db.Integer)
    municipio_id = db.Column(
        db.Integer,
        db.ForeignKey("municipios.id"),
        nullable=False
    )