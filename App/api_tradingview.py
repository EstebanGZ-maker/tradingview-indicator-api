from flask import Flask, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)  # ✅ Esto habilita CORS para todos los dominios

# Ruta al archivo JSON
JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'indicador_data.json')

@app.route('/data', methods=['GET'])
def get_data():
    try:
        with open(JSON_PATH, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({'error': 'Archivo indicador_data.json no encontrado'}), 404
    except json.JSONDecodeError:
        return jsonify({'error': 'Error al leer el JSON'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
