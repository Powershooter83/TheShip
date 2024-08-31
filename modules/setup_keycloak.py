import requests

from models.Environment import BASE_URL_LASER


def setup_keycloak():
    try:
        data = {"client_secret": "B7zJDGUaESVeIFeFpw4sn2KSzsgkuN9C",
                "authorize_url": "http://192.168.100.21:8080/realms/master/protocol/openid-connect/auth",
                "token_url": "http://192.168.100.21:8080/realms/master/protocol/openid-connect/token"}

        response = requests.post(f"{BASE_URL_LASER}configure_oauth", json=data)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)

print(setup_keycloak())