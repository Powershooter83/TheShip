from time import sleep

from opcua import Client

from models.Environment import BASE_URL_JUMPDRIVE
from models.Vector2 import Vector2
from modules.ScannerHandler import get_current_position


def jumpdrive(target_location: Vector2):
    with Client(url=BASE_URL_JUMPDRIVE) as client:
        obj = client.get_node("ns=0;i=20001")
        method = obj.get_child("0:JumpTo")
        get_charge_percent = obj.get_child("0:GetChargePercent")

        current_location = get_current_position()

        while current_location != target_location:
            dx = target_location.x - current_location.x
            dy = target_location.y - current_location.y

            if dx != 0:
                step_x = min(max(dx, -20000), 20000)
                result = obj.call_method(method, int(current_location.x + step_x), int(current_location.y))
                current_location.x += step_x
                print(f"Jump result (X): {result}")
            elif dy != 0:
                step_y = min(max(dy, -20000), 20000)
                result = obj.call_method(method, int(current_location.x), int(current_location.y + step_y))
                current_location.y += step_y
                print(f"Jump result (Y): {result}")

            while obj.call_method(get_charge_percent) != 1.0:
                print("Warte auf Aufladung...")
                sleep(5)

        print("Zielposition erreicht.")