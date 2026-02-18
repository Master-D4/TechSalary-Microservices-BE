import httpx
from fastapi import HTTPException
from app.core.config import settings
import json


class IdentityClient:
    async def forward_request(self, method: str, path: str, data: dict = None, headers: dict = None):
        url = f"{settings.IDENTITY_SERVICE_URL}{path}"

        async with httpx.AsyncClient() as client:
            try:
                # Enable follow_redirects=True to auto-fix slash issues
                response = await client.request(
                    method=method,
                    url=url,
                    json=data,
                    headers=headers,
                    follow_redirects=True
                )

                # Check if response content is empty before parsing
                if not response.content:
                    return {}, response.status_code

                try:
                    return response.json(), response.status_code
                except json.JSONDecodeError:
                    # If Identity Service returns HTML (like a 404 or 500 error page),
                    # return a safe error message instead of crashing.
                    return {"detail": response.text}, response.status_code

            except httpx.RequestError as exc:
                raise HTTPException(status_code=503, detail=f"Identity Service unavailable: {exc}")


identity_client = IdentityClient()