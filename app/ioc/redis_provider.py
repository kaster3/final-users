from typing import AsyncIterator

from redis import asyncio as aredis
from dishka import Provider, Scope, provide

from app.core import Settings


class RedisProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_redis(self, settings: Settings) -> AsyncIterator[aredis.Redis]:
        redis = aredis.from_url(str(settings.redis.url))
        try:
            yield redis
        finally:
            await redis.close()