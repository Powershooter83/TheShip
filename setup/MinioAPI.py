import base64
import io
import json
import uuid

import requests
from flask import Flask, jsonify
import boto3

from models.Station import StationEnum

app = Flask(__name__)

@app.route('/<station>/receive', methods=['POST'])
def receive(station):
    data = zurro_rest()
    print(transform_messages(json.loads(data.text).get('received_messages')))

    return jsonify({"kind": "success", "messages": f"Received station: {station}"})


@app.route('/<station>/send', methods=['POST'])
def send(station):
   print(station)

   return None

def zurro_rest():
    try:
        return requests.post(f"{StationEnum.ZURRO.value.get_url()}receive")
    except requests.exceptions.RequestException as e:
        raise e

data = zurro_rest()







def transform_messages(received_messages):
    transformed_messages = []

    for item in received_messages:
        dest = item["dest"]
        msg = item["msg"]

        decoded_bytes = base64.b64decode(msg)
        decoded_str = decoded_bytes.decode('utf-8')

        transformed_messages.append({
            "destination": dest,
            "data": decoded_str
        })

    return transformed_messages

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=2023, debug=True)
