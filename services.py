from typing import Any
import httpx
from fastapi import HTTPException


async def validate_artwork_id(external_id: int) -> Any:
    """Checks if the artwork ID exists in the Art Institute of Chicago API."""
    url = f"https://api.artic.edu/api/v1/artworks/{external_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=f"Place ID {external_id} not found in Art Institute API",
            )
        return response.json()
