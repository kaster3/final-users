from fastapi import status
from fastapi.exceptions import HTTPException

from app.api.api_v1.company.dto import CompanyCreate, CompanyUpdate
from app.core.database.models import Company
from app.core.database.models.enums.user_role import UserRole
from app.core.interfaces.company import IDBCompanyRepository
from app.core.services.user import UserService


class CompanyService:
    def __init__(
            self,
            compony_repository: IDBCompanyRepository,
            user_service: UserService,
    ) -> None:
        self.company_repository = compony_repository
        self.user_service = user_service

    async def create_company(
            self,
            company_data: CompanyCreate,
    ) -> Company:
        company = await self.company_repository.create_company(company_data=company_data)
        return company

    async def get_by_id(self, company_id: int) -> Company | None:
        company = await self.company_repository.get_by_id(company_id=company_id)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Company with id #{company_id} not exists!"
            )
        return company

    async def find_by_invite_code(self, invite_code) -> Company:
        company = await self.company_repository.get_by_invite_code(invite_code=invite_code)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid invite code."
            )
        return company

    async def update(self, company_id: int, user_data: CompanyUpdate) -> Company:
        company = await self.get_by_id(company_id=company_id)
        updated_company = await self.company_repository.update(
            company=company,
            user_data=user_data,
        )
        return updated_company


    async def add_user_in_company(
            self,
            company_id: int,
            user_id: int,
            role: UserRole = UserRole.MEMBER,
    ) -> None:
        company = await self.get_by_id(company_id=company_id)
        user = await self.user_service.get_user_by_id(user_id=user_id)

        if user in company.users:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already in company",
            )

        # TODO возможно тут лучше можно сделать, более абстрактно
        if user.role != role:
            user.role = role.value

        await self.company_repository.add_user(user=user, company=company)

    async def del_user_from_company(self, company_id: int, user_id: int) -> None:
        company = await self.get_by_id(company_id=company_id)
        user = await self.user_service.get_user_by_id(user_id=user_id)

        if user not in company.users:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User #{user_id} not in the company #{company_id}"
            )

        await self.company_repository.remove_user(
            user=user,
            company=company,
        )