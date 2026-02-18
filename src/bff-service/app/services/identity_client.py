import httpx
from fastapi import HTTPException
from app.core.config import settings


class IdentityClient:
    async def forward_request(self, method: str, path: str, data: dict = None, headers: dict = None):
        url = f"{settings.IDENTITY_SERVICE_URL}{path}"

        async with httpx.AsyncClient() as client:
            try:
                # We forward the request to the Identity Service
                response = await client.request(
                    method=method,
                    url=url,
                    json=data,
                    headers=headers
                )

                # We return the response content and status code exactly as is
                return response.json(), response.status_code

            except httpx.RequestError as exc:
                # Handle connection errors (e.g., Identity Service is down)
                raise HTTPException(status_code=503, detail=f"Identity Service unavailable: {exc}")


identity_client = IdentityClient()