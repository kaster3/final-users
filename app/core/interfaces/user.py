from abc import abstractmethod
from typing import Protocol

from app.api.api_v1.auth.dto import UserCreate
from app.core.database.models import User


class IUserRepository(Protocol):
    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def create_user(
            self,
            user_data: UserCreate,
            hashed_password: str,
            company_id: int | None,
    ) -> User:
        raise NotImplementedError