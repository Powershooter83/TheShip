from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_measurement():
    response = requests.get("http://192.168.100.21:2038/data")
    if response.status_code == 200:
        data = response.json()

        return jsonify({"data": data.get("measurement")})
    else:
        # Fehlerbehandlung, wenn der andere Endpoint nicht erreichbar ist
        return jsonify({"error": "Failed to retrieve data"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2101)
