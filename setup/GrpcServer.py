import grpc
from concurrent import futures
import requests
import threading
import time
import api_pb2 as pb2
import api_pb2_grpc as pb2_grpc
from modules.MeasurementHandler import trigger_measurement_and_store

# Globale Variable zur Speicherung der letzten Sensorantwort
response = ""


# Funktion zum periodischen Abrufen der Sensordaten
def fetch_sensor_data():
    global response
    while True:
        response = trigger_measurement_and_store()
        time.sleep(2)  # Beispiel für 5 Sekunden Wartezeit zwischen Abrufen


class SensorVoidEnergyServer(pb2_grpc.SensorVoidEnergyServerServicer):
    def read_sensor_data(self, request, context):
        try:
            # Senden der aktuellen Sensordaten
            return pb2.SensorData(hexdata=response)
        except requests.RequestException as e:
            context.set_details(f"Error fetching sensor data: {e}")
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            return pb2.SensorData()


def serve():
    # Starten des gRPC-Servers
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_SensorVoidEnergyServerServicer_to_server(SensorVoidEnergyServer(), server)
    server.add_insecure_port("[::]:2102")
    server.start()
    print("Server started on port 2102")

    # Starten des Threads für das Abrufen der Sensordaten
    data_fetch_thread = threading.Thread(target=fetch_sensor_data)
    data_fetch_thread.daemon = True
    data_fetch_thread.start()

    # Warten auf Serverbeendigung
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
