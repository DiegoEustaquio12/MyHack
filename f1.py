from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/receta", methods=["POST"])
def receta():
    datos = request.get_json()
    
    if not datos:
        error_msg = "No se pueden calcular valores negativos"
        return jsonify({
            "fertilizante": error_msg,
            "cantidad": error_msg,
            "costo": error_msg
        })

    try:
        hectareas = float(datos.get("hectareas", 0))
        
        if hectareas <= 0:
            error_msg = "No se pueden calcular valores negativos"
            return jsonify({
                "fertilizante": error_msg,
                "cantidad": error_msg,
                "costo": error_msg
            })

        cantidad = hectareas * 50
        costo = hectareas * 300

        return jsonify({
            "fertilizante": "Urea 46%",
            "cantidad": f"{cantidad} kg",
            "costo": f"${costo} MXN"
        })

    except (ValueError, TypeError):
        error_msg = "No se pueden calcular valores negativos"
        return jsonify({
            "fertilizante": error_msg,
            "cantidad": error_msg,
            "costo": error_msg
        })

if __name__ == "__main__":
    app.run(debug=True)
