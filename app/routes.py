from flask import Blueprint, jsonify
from .models import Municipio

main = Blueprint("main", __name__)
# Crea un grupo de rutas

@main.route("/")
def inicio():
    return "API funcionando"