from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    db.init_app(app)
    # Conecta la base de datos con Flask

    from .routes import main
    app.register_blueprint(main)
    # Activa las rutas en la app

    return app
    # Devuelve la app lista