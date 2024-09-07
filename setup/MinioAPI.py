from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/<station>/receive', methods=['POST'])
def receive(station):
    try:
        print(f"Received data at {station}:")
        return jsonify({"kind": "success", "messages": [{"destination": "Shangris Station", "data": [0, 1, 2, 3, 4]}]}), 200
    except Exception as e:
        return jsonify({"kind": "error", "message": str(e)}), 500

@app.route('/<station>/send', methods=['POST'])
def send(station):
    try:
        data = request.json
        if data is None:
            raise ValueError("No JSON data received")
        print(f"Sending data from {station}:", data)
        return jsonify({"kind": "success"}), 200
    except Exception as e:
        return jsonify({"kind": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2023, debug=True)
