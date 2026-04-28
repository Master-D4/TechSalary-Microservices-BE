import json

import httpx
from fastapi import HTTPException

from app.core.config import settings


class VoteClient:
    async def forward_request(
        self,
        method: str,
        path: str,
        data: dict | None = None,
        headers: dict | None = None,
    ):
        url = f"{settings.VOTE_SERVICE_URL}{path}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    json=data,
                    headers=headers,
                    follow_redirects=True,
                )

                if not response.content:
                    return {}, response.status_code

                try:
                    return response.json(), response.status_code
                except json.JSONDecodeError:
                    return {"detail": response.text}, response.status_code

            except httpx.RequestError as exc:
                raise HTTPException(
                    status_code=503,
                    detail=f"Vote Service unavailable: {exc}",
                ) from exc


vote_client = VoteClient()
