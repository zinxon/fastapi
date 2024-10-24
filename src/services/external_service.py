import httpx
from fastapi import HTTPException

class ExternalService:
    def __init__(self, base_url: str = "https://api.example.com"):
        self.base_url = base_url
        
    async def fetch_external_data(self, item_id: str) -> dict:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/items/{item_id}")
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                raise HTTPException(status_code=503, detail=f"External service error: {str(e)}")