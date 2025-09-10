import requests
from requests.exceptions import HTTPError, Timeout, RequestException

class ClientApi:
    BASE_URL = "https://api.ejemplo.com"
    TIMEOUT = 5  # segundos

    def __init__(self, api_key=None):
        self.headers = {
            "Authorization": f"Bearer {api_key}" if api_key else "",
            "Accept": "application/json"
        }

    def get_resource(self, resource_id):
        url = f"{self.BASE_URL}/resource/{resource_id}/"
        try:
            response = requests.get(url, headers=self.headers, timeout=self.TIMEOUT)
            response.raise_for_status()
            return response.json()
        except HTTPError as http_err:
            # Puedes hacer logging avanzado aquí
            print(f"HTTP error occurred: {http_err}")
            return None
        except Timeout:
            print("Request timed out")
            return None
        except RequestException as err:
            print(f"Other error occurred: {err}")
            return None
