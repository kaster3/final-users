import logging
import os
from asyncio import create_task
from contextlib import asynccontextmanager

from dishka import AsyncContainer
from fastapi import FastAPI
from redis import asyncio
from fastapi.responses import ORJSONResponse
from fastapi_admin.app import app as admin_app
from fastapi_admin.constants import BASE_DIR
from dishka.integrations.fastapi import setup_dishka
from fastapi_admin.providers.login import UsernamePasswordProvider

from app.api import router as api_router
from app.core import Settings
from app.core.database.models import User
from app.core.gunicorn import Application, get_app_options
from app.ioc.init_container import init_async_container


from tortoise.models import Model
from tortoise import fields

class Admin(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    is_active = fields.BooleanField(default=True)


login_provider = UsernamePasswordProvider(
        admin_model=Admin,
        login_logo_url="https://preview.tabler.io/static/logo.svg"
    )

async def startup(redis: asyncio.Redis):
    await admin_app.configure(
        logo_url="https://preview.tabler.io/static/logo-white.svg",
        template_folders=[os.path.join(BASE_DIR, "templates")],
        providers=[login_provider],
        redis=redis,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Application starts successfully!")
    container: AsyncContainer = app.state.dishka_container
    async with container() as requested_container:
        redis = await requested_container.get(asyncio.Redis)
        await startup(redis=redis)
    yield
    logging.info("Shutting down application...")
    await app.state.dishka_container.close()
    logging.info("Application ends successfully!")


def create_fastapi_app() -> FastAPI:
    """Создаем FastAPI приложение и настраиваем его на роутеры"""
    app = FastAPI(
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )
    app.include_router(
        router=api_router,
    )
    app.mount("/admin", admin_app)
    return app


def create_app(settings: Settings) -> FastAPI:
    """Настраиваем логи, контейнер с зависимостями и инициализируем наше приложение"""
    logging.basicConfig(
        level=settings.logging.log_level,
        format=settings.logging.log_format,
    )
    app = create_fastapi_app()
    container = init_async_container(settings=settings)
    setup_dishka(container, app)
    return app



# Запускаем приложение с uvicorn воркерами и gunicorn менеджера
if __name__ == "__main__":
    settings = Settings()
    Application(
        application=create_app(settings=settings),
        options=get_app_options(
            host=settings.gunicorn.host,
            port=settings.gunicorn.port,
            timeout=settings.gunicorn.timeout,
            workers=settings.gunicorn.workers,
            log_level=settings.logging.log_level,
        ),
    ).run()
