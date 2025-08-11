from sqlalchemy.ext.asyncio import AsyncSession

from app.api.api_v1.auth.dto import UserCreate
from app.core.database.models import User
from app.core.interfaces.user import IUserRepository


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        user = await self.session.get(User, user_id)
        return user

    async def create_user(
            self,
            user_data: UserCreate,
            hashed_password: str,
            company_id: int | None,
    ) -> User:

        user = User(
            **user_data.model_dump(exclude={"invite_code", "password"}),
            company_id=company_id,
            hashed_password=hashed_password,
        )

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
