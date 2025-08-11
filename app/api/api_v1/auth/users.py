from fastapi import APIRouter

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