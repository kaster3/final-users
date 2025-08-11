from dishka import AsyncContainer, make_async_container

from app.core import Settings
from app.ioc.redis_provider import RedisProvider
from app.ioc.service_provider import ServiceProvider
from app.ioc.sqlalchemy_providers import SQLAlchemyProvider


def init_async_container(settings: Settings) -> AsyncContainer:
    container = make_async_container(
        SQLAlchemyProvider(),
        ServiceProvider(),
        RedisProvider(),
        context={
            Settings: settings,
        }
    )
    return container
