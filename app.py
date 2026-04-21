from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    
    
@app.route("/equipo")
def equipo():
    return "<h1> Somos 4 y ganaremos <h1>"

