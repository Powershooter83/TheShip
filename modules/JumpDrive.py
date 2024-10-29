from opcua import Client

from models.Environment import BASE_URL_JUMPDRIVE
from models.Vector2 import Vector2

def jumpdrive(location: Vector2):
    with Client(url=BASE_URL_JUMPDRIVE) as client:
        obj = client.get_node("ns=0;i=20001")
        method = obj.get_child("0:JumpTo")
        obj.call_method(method, location.x, location.y)
