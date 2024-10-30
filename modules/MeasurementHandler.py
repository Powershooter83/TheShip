import requests
import time
from pymongo import MongoClient


def trigger_measurement_and_store():
    client = MongoClient("mongodb://theship:theship1234@192.168.100.21:2021/theshipdb")
    db = client['theshipdb']
    collection = db['vacuum-energy']


    trigger_url = "http://192.168.100.21:2037/trigger_measurement"
    data = {"request_id": "my_id_001"}
    response = requests.post(trigger_url, json=data)

    if response.status_code == 201:
        print("Messung erfolgreich angefordert.")
    else:
        print(f"Fehler beim Anfordern der Messung: {response.status_code}")
        return

    # 2. Messungsstatus abrufen
    measurement_url = "http://192.168.100.21:2037/measurements/my_id_001"
    while True:
        response = requests.get(measurement_url)
        result = response.json()

        if result["state"] == "measured":
            print("Messung abgeschlossen.")
            break
        else:
            print("Messung läuft...")
            time.sleep(2)  # Wartezeit für erneute Abfragen

    # 3. Ergebnis speichern
    if "result" in result:
        collection.delete_many({})
        collection.insert_one({
            "data": result["result"]
        })
        print("Messungsergebnis in MongoDB gespeichert.")
    else:
        print("Kein Messergebnis vorhanden.")

    # 4. Messung löschen
    delete_response = requests.delete(measurement_url)
    if delete_response.status_code == 200:
        print("Messung erfolgreich gelöscht.")
    else:
        print(f"Fehler beim Löschen der Messung: {delete_response.status_code}")

    # Verbindung zur MongoDB schließen
    client.close()


# Methode ausführen
trigger_measurement_and_store()
