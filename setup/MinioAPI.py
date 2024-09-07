import base64
import io
import json
import uuid

import requests
from flask import Flask, jsonify
import boto3

from models.Environment import BASE_URL_ZURRO

app = Flask(__name__)

# MinIO-Konfiguration
MINIO_ENDPOINT = 'http://192.168.100.21:2016'
MINIO_ACCESS_KEY = 'theship'
MINIO_SECRET_KEY = 'theship1234'
BUCKET_NAME = 'theship-permastore'

s3_client = boto3.client(
    's3',
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY
)


@app.route('/<station>/receive', methods=['POST'])
def receive(station):
    data = zurro_rest()
    transform_message = transform_messages(json.loads(data.text).get('received_messages'))
 #   json_bytes = json.dumps(transform_message).encode('utf-8')
  #  print(json_bytes)

    # s3_client.put_object(
    #     Bucket=BUCKET_NAME,
    #     Key=str(uuid.uuid4()),
    #     Body=io.BytesIO(json_bytes),
    #     ContentType='application/json'
    # )



    return jsonify({"kind": "success", "messages": "result"}), 200

def zurro_rest():
    try:
        return requests.post(f"{BASE_URL_ZURRO}receive")
    except requests.exceptions.RequestException as e:
        raise e


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



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2023, debug=True)
