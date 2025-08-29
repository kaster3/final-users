from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status, Query, Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.core.authentication.methods import verify_api_key, http_bearer
from app.core.database.models.enums.user_role import UserRole
from app.core.services.permissions import CheckPermission
from app.core.services.user import UserService
from app.core.settings import settings
from app.api.api_v1.auth.dependencies.my_fastapi_users import fastapi_users
from .dto import UserCreate, UserRead

router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],
)

# /me
# /{id}
router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserCreate,
        requires_verification=True,
    ),
)

@router.get(
    "/service/{user_id}",
    dependencies=[Depends(verify_api_key)]
)
@inject
async def get_user_by_id_service(
        user_id: int,
        service: FromDishka[UserService],
):
    return await service.get_user_by_id(user_id=user_id)


@router.patch(
    path="/change_role/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
)
@inject
async def change_user_company_role(
        user_id: int,
        service: FromDishka[UserService],
        perm: FromDishka[CheckPermission],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
        role: UserRole = Query(...),
):
    #TODO сейчас любой superuser может изменить роль сотрудника любой компании,
    # нужно сделать проверку что изменяющий из той же компании, что и изменяемый
    await perm.check_is_admin_or_superuser(
        token=credentials.credentials,
    )
    user = await service.change_user_role(user_id=user_id, role=role)
    return user

