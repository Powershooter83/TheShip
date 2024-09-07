from flask import Flask, request, jsonify

app = Flask(__name__)

# Endpoint zum Empfangen von Daten
@app.route('/<station>/receive', methods=['POST'])
def receive(station):
    data = request.json
    # Hier kannst du die Logik für die Verarbeitung der empfangenen Daten hinzufügen
    print(f"Received data at {station}:", data)
    return jsonify({"kind": "success", "messages": [{"destination": "Shangris Station", "data": [0, 1, 2, 3, 4]}]}), 200

# Endpoint zum Senden von Daten
@app.route('/<station>/send', methods=['POST'])
def send(station):
    data = request.json
    print(f"Sending data from {station}:", data)
    return jsonify({"kind": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2023)
