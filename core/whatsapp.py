import httpx
from core.config import settings

class EvolutionAPI:
    def __init__(self):
        self.base_url = settings.EVOLUTION_API_URL
        self.api_key = settings.EVOLUTION_API_KEY
        self.instance_name = settings.EVOLUTION_INSTANCE_NAME
        self.headers = {
            "apikey": self.api_key,
            "Content-Type": "application/json"
        }

    async def send_message(self, number: str, text: str):
        url = f"{self.base_url}/message/sendText/{self.instance_name}"
        payload = {
            "number": number,
            "text": text
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def send_media(self, number: str, text: str, media_url: str):
        url = f"{self.base_url}/message/sendMedia/{self.instance_name}"
        payload = {
            "number": number,
            "mediaMessage": {
                "mediatype": "document",
                "caption": text,
                "media": media_url,
            }
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()

whatsapp = EvolutionAPI()
