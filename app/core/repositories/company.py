from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.api_v1.company.dto import CompanyCreate, CompanyUpdate
from app.core.database.models import Company, User
from app.core.interfaces.company import IDBCompanyRepository


class SQLAlchemyCompanyRepository(IDBCompanyRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_company(self, company_data: CompanyCreate,) -> Company:
        company = Company(**company_data.model_dump())
        self.session.add(company)
        await self.session.commit()
        await self.session.refresh(company)
        return company

    async def get_by_id(self, company_id: int) -> Company | None:
        stmt = select(Company).where(Company.id == company_id).options(
            selectinload(Company.users)
        )
        company = await self.session.scalar(stmt)
        return company

    async def get_by_invite_code(self, invite_code: str) -> Company | None:
        stmt = select(Company).where(Company.invite_code == invite_code)
        result = await self.session.scalar(stmt)
        return result

    async def update(self, company: Company, user_data: CompanyUpdate) -> Company:
        for name, value in user_data.model_dump(exclude_unset=True).items():
            setattr(company, name, value)
        await self.session.commit()
        return company

    async def add_user(self, company: Company, user: User) -> None:
        company.users.append(user)
        await self.session.commit()

    async def remove_user(self, company: Company, user: User) -> None:
        company.users.remove(user)
        await self.session.commit()

