from datetime import datetime

from fastapi import APIRouter
from fastapi import Request

router = APIRouter()

CACHE_KEY = "test:cache"


@router.get("/cache")
async def cache_test(
    request: Request,
):

    redis_client = request.app.state.redis

    cached = await redis_client.get(
        CACHE_KEY
    )

    if cached:

        return {
            "cached": True,
            "value": cached,
        }

    value = (
        datetime.utcnow()
        .isoformat()
    )

    await redis_client.set(
        CACHE_KEY,
        value,
        ex=300,
    )

    return {
        "cached": False,
        "value": value,
    }


@router.get("/no-cache")
async def no_cache_test():

    return {
        "cached": False,
        "value": datetime.utcnow().isoformat(),
    }