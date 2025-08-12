from abc import abstractmethod

from typing import Protocol

from app.api.api_v1.company.dto import CompanyCreate
from app.core.database.models import Company, User


class IDBCompanyRepository(Protocol):
    @abstractmethod
    async def create_company(
            self,
            company_data: CompanyCreate,
    ) -> Company:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, company_id: int) -> Company | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_invite_code(self, invite_code: str) -> Company | None:
        raise NotImplementedError

    @abstractmethod
    async def add_user(self, company: Company, user: User) -> None:
        """Добавить пользователя в компанию"""
        raise NotImplementedError

    @abstractmethod
    async def remove_user(self, company: Company, user: User) -> None:
        """Удалить пользователя из компании"""
        raise NotImplementedError

    @abstractmethod
    async def update_user_role(self, user: User, new_role: str) -> None:
        """Изменить роль пользователя в компании"""
        raise NotImplementedError
