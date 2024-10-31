import grpc
from concurrent import futures
import requests
import api_pb2 as pb2
import api_pb2_grpc as pb2_grpc

# Implementiere den gRPC-Server
class SensorVoidEnergyServer(pb2_grpc.SensorVoidEnergyServerServicer):
    def read_sensor_data(self, request, context):
        # Lade Daten vom Atom-Feldsensor herunter
        try:
            response = requests.get("http://192.168.100.21:2038/data")
            response.raise_for_status()  # Check für HTTP-Fehler
            hex_data = response.text  # Annahme: Daten sind im Textformat
            return pb2.SensorData(hexdata=hex_data)
        except requests.RequestException as e:
            context.set_details(f"Error fetching sensor data: {e}")
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            return pb2.SensorData()  # Rückgabe eines leeren SensorData-Objekts

# Startet den gRPC-Server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_SensorVoidEnergyServerServicer_to_server(SensorVoidEnergyServer(), server)
    server.add_insecure_port("[::]:2102")
    server.start()
    print("Server started on port 2102")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
