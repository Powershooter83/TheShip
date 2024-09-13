import grpc
import api_pb2
import api_pb2_grpc

def run():
    # Die Adresse des gRPC-Servers
    server_address = '192.168.100.21:2028'

    # Erstelle einen Kanal zum gRPC-Server
    with grpc.insecure_channel(server_address) as channel:
        # Erstelle einen Stub für den Service
        stub = api_pb2_grpc.HackingDeviceServerStub(channel)

        # Erstelle eine leere Anfrage
        request = api_pb2.Void()

        try:
            # Rufe die Methode auf
            response = stub.read_secret_station_data(request)

            # Gib die Antwort aus
            print("Received data:", response.data)

        except grpc.RpcError as e:
            print(f"gRPC error: {e.code()} - {e.details()}")

if __name__ == '__main__':
    run()
