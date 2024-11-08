import requests
from flask import Flask
app = Flask(__name__)

@app.route(rule="/", methods=["GET"])
def get_data():
    try:
        response = requests.get("http://192.168.100.21:2038/data", timeout=1)
        json = response.json()
        return {"data": json.get("atomic_field_value")}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2101)
