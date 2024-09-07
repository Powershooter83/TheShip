import json
import uuid

from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

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

@app.route('/<station>/send', methods=['POST'])
def send(station):
    try:
        data = request.json
        if data is None:
            raise ValueError("No JSON data received")

        unique_id = str(uuid.uuid4())
        file_name = f"{station}_{unique_id}.json"

        s3_client.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=str(data))
        return jsonify({"kind": "success"}), 200
    except NoCredentialsError:
        return jsonify({"kind": "error", "message": "Credentials not available"}), 403
    except PartialCredentialsError:
        return jsonify({"kind": "error", "message": "Incomplete credentials provided"}), 403
    except Exception as e:
        return jsonify({"kind": "error", "message": str(e)}), 500

@app.route('/<station>/receive', methods=['POST'])
def receive(station):
    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        files = response.get('Contents', [])
        result = []
        for file in files:
            file_key = file['Key']
            obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_key)
            file_data = obj['Body'].read().decode('utf-8')

            try:
                json_data = json.loads(file_data)
            except json.JSONDecodeError:
                continue

            print(json_data)
            if json_data.get('source') == station:
                result.append({
                    "file": file_key,
                    "data": json_data
                })

        if not result:
            return jsonify({"kind": "error", "message": "No data found for the specified source"}), 404

        return jsonify({"kind": "success", "messages": result}), 200
    except ValueError as e:
        return jsonify({"kind": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"kind": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2023, debug=True)
