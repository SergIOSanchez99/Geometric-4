from flask import Flask, render_template
import JuegoModificado  # Importa tu archivo aquí

app = Flask(__name__)

@app.route('/')
def index():
    # Aquí puedes llamar a funciones de tu juego o pasar datos a la plantilla
    return render_template('index.html')  # Asegúrate de que este archivo HTML exista

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Para ejecutar localmente
