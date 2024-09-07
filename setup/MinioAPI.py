import json

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
    json.loads(data)
    print(data)


    return jsonify({"kind": "success", "messages": "result"}), 200

def zurro_rest():
    try:
        return requests.post(f"{BASE_URL_ZURRO}download")
    except requests.exceptions.RequestException as e:
        raise e


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2023, debug=True)
