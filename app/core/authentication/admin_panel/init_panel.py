from dishka import AsyncContainer
from fastapi import FastAPI
from fastapi_users.password import PasswordHelper
from sqladmin import Admin

from app.core import Settings
from app.core.authentication.admin_panel.auth import AdminAuth
from app.core.authentication.admin_panel.models import UserAdmin
from app.core.database.db_helper import DataBaseHelper
from app.core.interfaces.user import IUserRepository


async def init_admin_panel(container: AsyncContainer, app: FastAPI) -> None:
    async with container() as requested_container:
        engine = await requested_container.get(DataBaseHelper)
        user_repository = await requested_container.get(IUserRepository)
        password_helper = await requested_container.get(PasswordHelper)
        settings = await requested_container.get(Settings)
        admin = Admin(
            app,
            engine.engine,
            authentication_backend=AdminAuth(
                secret_key=settings.admin_panel.SECRET_KEY,
                user_repository=user_repository,
                password_helper=password_helper,
            ),
        )

        admin.add_view(UserAdmin)