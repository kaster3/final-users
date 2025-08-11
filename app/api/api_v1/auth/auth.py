from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import status, APIRouter, Request, Depends

from app.api.api_v1.auth.dto import UserRead, UserCreate, UserUpdate
from app.core.database.models import User
from app.core.services.user import UserService
from app.core.settings import settings
from app.api.api_v1.auth.dependencies.backend import authentication_backend
from app.api.api_v1.auth.dependencies.my_fastapi_users import fastapi_users

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
)

# /login, /logout
router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
        requires_verification=False,
    ),
)

# /register
@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead,
)
@inject
async def user_register(
        user_data: UserCreate,
        request: Request,
        service: FromDishka[UserService],
):
    return await service.create_user(request=request, user_data=user_data)



# /request-verify-token
# /verify
router.include_router(
    router=fastapi_users.get_verify_router(
        UserRead,
    ),
)

# forgot-password
# reset-password
router.include_router(
    router=fastapi_users.get_reset_password_router(),
)