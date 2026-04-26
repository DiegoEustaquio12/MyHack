from flask import Blueprint, jsonify, render_template
from .models import Municipio

main = Blueprint("main", __name__)
# Crea un grupo de rutas

@main.route("/")
def inicio():
    return render_template("index.html")