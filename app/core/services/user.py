from fastapi import Request, status, HTTPException
from fastapi_users.password import PasswordHelper

from app.api.api_v1.auth.dto import UserCreate
from app.core.database.models import User
from app.core.database.models.enums.user_role import UserRole
from app.core.interfaces.company import IDBCompanyRepository
from app.core.interfaces.user import IUserRepository
from app.core.services.jwt import JWTHelper


class UserService:
    def __init__(
            self,
            # company_service: CompanyService,
            user_repository: IUserRepository,
            company_repository: IDBCompanyRepository,
            password_helper: PasswordHelper,
            jwt_helper: JWTHelper,
    ) -> None:
        # self.company_service = company_service
        self.user_repository = user_repository
        self.company_repository = company_repository
        self.password_helper = password_helper
        self.jwt_helper = jwt_helper

    async def create_user(
            self,
            request: Request,
            user_data: UserCreate,
            company_id: None = None
    ) -> User:
        hashed_password = self.password_helper.hash(user_data.password)

        if user_data.is_superuser or user_data.is_verified:
            if token := request.headers.get("Authorization"):
                user_id = self.jwt_helper.get_user_id(token=token)
                user = await self.user_repository.get_user_by_id(user_id=user_id)
                if not user.is_superuser:
                    user_data.is_superuser = False
                    user_data.is_verified = False
            else:
                user_data.is_superuser = False
                user_data.is_verified = False

        if invite_code := user_data.invite_code:
            if not (company := await self.company_repository.get_by_invite_code(invite_code=invite_code)):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or expired invite code"
                )
            company_id = company.id

        user = await self.user_repository.create_user(
            user_data=user_data,
            hashed_password=hashed_password,
            company_id=company_id
        )
        return user

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.user_repository.get_user_by_id(user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id #{user_id} does not exist",
            )
        return user

    async def change_user_role(self, user_id: int, role: UserRole) -> User:
        user = await self.get_user_by_id(user_id=user_id)
        updated_user = await self.user_repository.update_role(user=user, role=role)
        return updated_user





