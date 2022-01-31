import logging
from typing import Optional

import aioredis
from aioredis import Redis

from core.config import settings

logger = logging.getLogger(__name__)


client: Optional[Redis] = None


async def get_redis() -> Redis:
    return client


async def startup() -> Redis:
    pool = aioredis.ConnectionPool.from_url(settings.redis_uri)
    client = aioredis.Redis(connection_pool=pool)

    try:
        ping = await client.ping()
        if ping is True:
            return client
    except aioredis.AuthenticationError as exc:
        logger.exception(exc)
    except aioredis.ConnectionError as exc:
        logger.exception(exc)


async def shutdown() -> None:
    await client.close()
