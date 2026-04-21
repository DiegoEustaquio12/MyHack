from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/receta", methods=["POST"])
def receta():
    datos = request.get_json()
    try:
        hectareas = float(datos.get("hectareas", 0))
        # Limpiamos el texto del cultivo
        cultivo = str(datos.get("cultivo", "")).lower().strip()
        
        msg = "No se pueden calcular valores negativos"

        # Validación de números
        if hectareas <= 0:
            return jsonify({"fertilizante": msg, "cantidad": msg, "costo": msg})

        # Lógica de precios por cultivo (incluimos variantes por la 'ñ' o acentos)
        if cultivo in ["maíz", "maiz"]:
            precio = 300
        elif cultivo in ["caña", "cana"]:
            precio = 250
        else:
            # Si el cultivo no coincide, devolvemos el mensaje solicitado
            return jsonify({"fertilizante": msg, "cantidad": msg, "costo": msg})

        cantidad = hectareas * 50
        costo = hectareas * precio

        return jsonify({
            "fertilizante": "Urea 46%",
            "cantidad": f"{cantidad} kg",
            "costo": f"${costo} MXN"
        })

    except (ValueError, TypeError):
        msg = "No se pueden calcular valores negativos"
        return jsonify({"fertilizante": msg, "cantidad": msg, "costo": msg})

if __name__ == "__main__":
    app.run(debug=True)
