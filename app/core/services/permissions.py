from fastapi import HTTPException, status

from app.core.database.models.enums.user_role import UserRole
from app.core.services.jwt import JWTHelper
from app.core.services.user import UserService

class CheckPermission:
    def __init__(
            self,
            jwt_helper: JWTHelper,
            user_service: UserService,
    ) -> None:
        self.jwt_helper = jwt_helper
        self.user_service = user_service

    async def check_is_admin_or_superuser(
            self,
            token: str,
            company_id: int | None = None,
            only_admin: bool = False,
    ) -> None:
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized",
            )

        user_id = self.jwt_helper.get_user_id(token=token)
        user = await self.user_service.get_user_by_id(user_id=user_id)
        if not only_admin:
            if not (user.is_superuser or (user.role == UserRole.SUPERUSER and user.company.id == company_id)):
                self._insufficient_permissions_error()
        else:
            if not user.is_superuser:
                self._insufficient_permissions_error()


    @staticmethod
    def _insufficient_permissions_error() -> HTTPException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )



