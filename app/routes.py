from flask import Blueprint, jsonify, render_template
from .models import Cultivo, Idoneo, MunicipioCultivo

main = Blueprint("main", __name__)

@main.route("/")
def inicio():
    return render_template("index.html")