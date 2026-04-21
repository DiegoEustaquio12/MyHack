from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/receta", methods=["POST"])
def receta():
    datos = request.get_json()
    cultivo = datos.get("cultivo")
    hectareas = datos.get("hectareas")

    return jsonify({
        "fertilizante": "Urea 46%",
        "cantidad": f"{float(hectareas) * 50} kg",
        "costo": f"${float(hectareas) * 300} MXN"
    })

if __name__ == "__main__":
    app.run(debug=True)