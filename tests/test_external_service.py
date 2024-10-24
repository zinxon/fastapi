import pytest
from httpx import AsyncClient
from src.services.external_service import ExternalService
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_external_service_error():
    service = ExternalService(base_url="https://nonexistent.example.com")
    with pytest.raises(HTTPException) as exc_info:
        await service.fetch_external_data("test-id")
    assert exc_info.value.status_code == 503