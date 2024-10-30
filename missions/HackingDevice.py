import grpc
import api_pb2
import api_pb2_grpc
from models.Environment import BASE_URL_HACKING_DEVICE


def run():
    with grpc.insecure_channel(BASE_URL_HACKING_DEVICE) as channel:
        stub = api_pb2_grpc.HackingDeviceServerStub(channel)

        request = api_pb2.Void()

        try:
            response = stub.read_secret_station_data(request)
            print("Received data:", response.data)

        except grpc.RpcError as e:
            print(f"gRPC error: {e.code()} - {e.details()}")

if __name__ == '__main__':
    run()
