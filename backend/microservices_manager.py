import requests
from typing import Dict

class MicroserviceManager:
    def __init__(self):
        self.services = {
            'auth': 'http://localhost:31001',
            'mail': 'http://localhost:31002',
            'storage': 'http://localhost:31003',
            'settings': 'http://localhost:31004'
        }
    
    async def call_service(self, service: str, endpoint: str, method='GET', data=None) -> Dict:
        url = f"{self.services[service]}/{endpoint}"
        try:
            response = requests.request(method, url, json=data)
            return response.json()
        except Exception as e:
            return {'error': str(e)}
