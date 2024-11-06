import requests
import time

from modules.ScannerHandler import get_current_position


def rotate_spaceShip(target_rotation: float):
    # URLs der Thruster und Navigation
    navigation_url = "http://192.168.100.21:2010/pos"
    thruster_front_left_url = "http://192.168.100.21:2005/thruster"
    thruster_front_right_url = "http://192.168.100.21:2006/thruster"

    # Thrust-Leistung für grobe und feine Anpassungen
    high_thrust = 30  # für grobe Drehungen
    low_thrust = 10  # für feine Anpassungen
    correction_thrust = 5  # für Gegen-Thrust

    def set_thruster(url, power):
        requests.put(url, json={"thrust_percent": power})

    def get_current_angle():
        response = requests.get(navigation_url)
        if response.status_code == 200:
            return response.json()["pos"]["angle"]
        else:
            print("Fehler beim Abrufen der Position")
            return None

    # Start: aktueller Winkel
    current_angle = get_current_angle()
    if current_angle is None:
        return

    # Hauptschleife für Rotation
    while True:
        # Berechne den Drehwinkel und die kürzeste Richtung
        angle_difference = (target_rotation - current_angle + 180) % 360 - 180
        if abs(angle_difference) <= 0.1:  # Ziel erreicht mit 0,1 Grad Toleranz
            break

        # Rotation und Leistung abhängig von der Entfernung zum Ziel setzen
        rotation_direction = 1 if angle_difference > 0 else -1
        thrust_power = high_thrust if abs(angle_difference) > 5 else low_thrust

        # Thruster auf Basis der Richtung aktivieren
        if rotation_direction > 0:
            set_thruster(thruster_front_left_url, thrust_power)
            set_thruster(thruster_front_right_url, 0)
        else:
            set_thruster(thruster_front_right_url, thrust_power)
            set_thruster(thruster_front_left_url, 0)

        # Kurze Wartezeit und neuen Winkel abrufen
        time.sleep(0.1)
        current_angle = get_current_angle()
        if current_angle is None:
            break

        # Neue Differenz berechnen
        angle_difference = (target_rotation - current_angle + 180) % 360 - 180
        print(f"Aktueller Winkel: {current_angle}, Ziel: {target_rotation}, Differenz: {angle_difference}")

        # Gegen-Thrust anwenden, falls nahe am Ziel
        if abs(angle_difference) < 0.5:
            if rotation_direction > 0:
                set_thruster(thruster_front_right_url, correction_thrust)
            else:
                set_thruster(thruster_front_left_url, correction_thrust)
            time.sleep(0.05)

        # Thruster vollständig deaktivieren
        set_thruster(thruster_front_left_url, 0)
        set_thruster(thruster_front_right_url, 0)

    # Endgültiges Stoppen der Thruster
    set_thruster(thruster_front_left_url, 0)
    set_thruster(thruster_front_right_url, 0)
    print("Rotation abgeschlossen")


# Beispielaufruf
#rotate_spaceShip(0)


def steer_right(percentage: int):
    front_left = "http://192.168.100.21:2005/thruster"
    bottom_left = "http://192.168.100.21:2007/thruster"
    data = {"thrust_percent": percentage}
    requests.put(front_left, json=data)
    requests.put(bottom_left, json=data)

def steer_left(percentage: int):
    front_left = "http://192.168.100.21:2008/thruster"
    bottom_left = "http://192.168.100.21:2006/thruster"
    data = {"thrust_percent": percentage}
    requests.put(front_left, json=data)
    requests.put(bottom_left, json=data)

def stop_thrusters():
    steer_right(0)
    steer_left(0)

import requests
import time

def steer_right(percentage: int):
    front_left = "http://192.168.100.21:2005/thruster"
    bottom_left = "http://192.168.100.21:2007/thruster"
    data = {"thrust_percent": percentage}
    requests.put(front_left, json=data)
    requests.put(bottom_left, json=data)

def steer_left(percentage: int):
    front_left = "http://192.168.100.21:2008/thruster"
    bottom_left = "http://192.168.100.21:2006/thruster"
    data = {"thrust_percent": percentage}
    requests.put(front_left, json=data)
    requests.put(bottom_left, json=data)

def stop_thrusters():
    steer_right(0)
    steer_left(0)


steer_right(100)