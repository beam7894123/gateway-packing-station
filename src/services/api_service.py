import requests
from services.config_manager import ConfigManager

class APIService:
    @staticmethod
    def get_api_url():
        # Fetch the API URL from the ConfigManager
        config_manager = ConfigManager()
        return config_manager.get_api_url()

    @staticmethod
    def get_data(endpoint):
        API_URL = APIService.get_api_url()
        response = requests.get(f"{API_URL}{endpoint}")
        return response.json()

    @staticmethod
    def post_data(endpoint, data):
        API_URL = APIService.get_api_url()
        response = requests.post(f"{API_URL}{endpoint}", json=data)
        return response.json() if response.status_code == 201 else None
