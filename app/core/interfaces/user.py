from abc import abstractmethod
from typing import Protocol

from app.api.api_v1.auth.dto import UserCreate
from app.core.database.models import User
from app.core.database.models.enums.user_role import UserRole


class IUserRepository(Protocol):
    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def create_user(
            self,
            user_data: UserCreate,
            hashed_password: str,
            company_id: int | None,
    ) -> User:
        raise NotImplementedError

    @abstractmethod
    async def update_role(self, user: User, role: UserRole) -> User:
        raise NotImplementedError