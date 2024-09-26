FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY setup/MinioAPI.py .
COPY models ./models/

EXPOSE 2023

CMD ["python", "MinioAPI.py"]
