from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    # Crea las tablas que no existan (incluye la nueva tabla "parcelas")
    with app.app_context():
        from . import models          # noqa: F401 — importar para que SQLAlchemy registre los modelos
        db.create_all()

    return app