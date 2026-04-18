import httpx
from fastapi import HTTPException
from app.core.config import settings
import json


class StatsClient:
    async def forward_request(self, method: str, path: str, params: dict = None, headers: dict = None):
        url = f"{settings.STAT_SERVICE_URL}{path}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    params=params,
                    headers=headers,
                    follow_redirects=True
                )

                if not response.content:
                    return {}, response.status_code

                try:
                    return response.json(), response.status_code
                except json.JSONDecodeError:
                    return {"detail": response.text}, response.status_code

            except httpx.RequestError as exc:
                raise HTTPException(status_code=503, detail=f"Stats Service unavailable: {exc}")


stats_client = StatsClient()