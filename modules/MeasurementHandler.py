import uuid

import requests
import time
from pymongo import MongoClient


def trigger_measurement_and_store():
    client = MongoClient("mongodb://theship:theship1234@192.168.100.21:2021/theshipdb")
    db = client['theshipdb']
    collection = db['vacuum-energy']

    random = str(uuid.uuid4())


    trigger_url = "http://192.168.100.21:2037/trigger_measurement"
    data = {"request_id": random}
    response = requests.post(trigger_url, json=data)

    if response.status_code == 201:
        print("Messung erfolgreich angefordert.")
    else:
        print(response.text)
        print(f"Fehler beim Anfordern der Messung: {response.status_code}")
        return

    # 2. Messungsstatus abrufen
    measurement_url = "http://192.168.100.21:2037/measurements/" + random
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
    result2Return = ""
    if "result" in result:
        collection.delete_many({})
        result2Return = result["result"]
        collection.insert_one({
            "data": result2Return
        })
        print("Messungsergebnis in MongoDB gespeichert.")
    else:
        print("Kein Messergebnis vorhanden.")

    # 4. Messung löschen
    delete_response = requests.delete(measurement_url)
    print(delete_response)
    if delete_response.status_code == 200:
        print("Messung erfolgreich gelöscht.")
    else:
        print(f"Fehler beim Löschen der Messung: {delete_response.status_code}")

    client.close()
    return result2Return

