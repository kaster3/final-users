from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.models import Company, User
from app.core.interfaces.company import IDBCompanyRepository


class SQLAlchemyCompanyRepository(IDBCompanyRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_company(self, request,) -> Company:
        company = Company(**request.model_dump())
        self.session.add(company)
        await self.session.commit()
        await self.session.refresh(company)
        return company

    async def get_by_id(self, company_id: int) -> Company | None:
        company = await self.session.get(Company, company_id)
        return company

    async def get_by_invite_code(self, invite_code: str) -> Company | None:
        stmt = select(Company).where(Company.invite_code == invite_code)
        result = await self.session.scalar(stmt)
        return result

    async def add_user(self, company: Company, user: User) -> None:
        pass

    async def remove_user(self, company: Company, user: User) -> None:
        pass

    async def update_user_role(self, user: User, new_role: str) -> None:
        pass
