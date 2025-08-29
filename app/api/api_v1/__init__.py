from fastapi import APIRouter

from app.core import settings
from .some_endpoint import router as endpoint
from .auth.auth import router as auth
from .auth.users import router as users
from .company.handler import router as company


router = APIRouter(
    prefix=settings.api.v1.prefix,
)

for rout in (endpoint, auth, users, company):
    router.include_router(
        router=rout,
    )


@router.get("")
async def root():
    return {"message": "this path is http://127.0.0.1:8000/api/v1"}
