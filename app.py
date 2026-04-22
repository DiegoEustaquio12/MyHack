import webbrowser
import threading

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Esto espera 1 segundo y abre la URL automáticamente
threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:5000")).start()

if __name__ == '__main__':
    app.run(debug=True)
    
    
@app.route("/equipo")
def equipo():
    return "<h1> Somos 4 y ganaremos <h1>"

