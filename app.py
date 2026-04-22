import webbrowser
import threading

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/equipo")
def equipo():
    return "<h1> Somos 4 y ganaremos <h1>"

@app.route('/receta', methods=['POST'])
def calcular_receta():
    
    datos = request.get_json()
    
    cultivo = datos.get('cultivo')
    hectareas = float(datos.get('hectareas')) 
    tiempo = datos.get('tiempo')
    
    cantidad_calculada = hectareas * 150
    costo_calculado = hectareas * 3500

    
    return jsonify({
        "fertilizante": "Urea Premium y Fósforo",
        "cantidad": f"{cantidad_calculada} kg",
        "costo": f"${costo_calculado} MXN"
    })

# Esto espera 1 segundo y abre la URL de manera automatica 
threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:5000")).start()

if __name__ == '__main__':
    app.run(debug=True)
    
    


