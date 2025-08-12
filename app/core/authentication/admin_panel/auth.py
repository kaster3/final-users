import logging

from fastapi_users.password import PasswordHelper
from itsdangerous import URLSafeSerializer
from sqladmin.authentication import AuthenticationBackend
from fastapi import Request

from app.core.interfaces.user import IUserRepository


log = logging.getLogger(__name__)


class AdminAuth(AuthenticationBackend):
    def __init__(
            self,
            user_repository: IUserRepository,
            secret_key: str,
            password_helper: PasswordHelper
    ) -> None:
        self.serializer = URLSafeSerializer(secret_key)
        self.user_repository = user_repository
        self.password_helper = password_helper
        super().__init__(secret_key=secret_key)

    async def login(self, request: Request) -> bool:
        form = await request.form()
        email = form.get("username")
        password = form.get("password")
        user = await self.user_repository.get_user_by_email(email=email)
        if not user:
            self.password_helper.hash(password)  # Защита от timing-атаки
            return False

        verified, updated_hash = self.password_helper.verify_and_update(
            password, user.hashed_password
        )
        if not verified:
            log.warning("Not valid password")
            return False

        if not user.is_superuser:
            log.warning("%s is not a admin", user.email)
            return False

        token = self.serializer.dumps(str(user.id))
        request.session["admin_token"] = token
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("admin_token")
        if not token:
            return False

        try:
            user_id = int(self.serializer.loads(token))
        except:
            return False

        user = await self.user_repository.get_user_by_id(user_id=user_id)
        return bool(user and user.is_superuser)