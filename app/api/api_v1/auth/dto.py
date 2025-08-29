from fastapi_users import schemas
from pydantic import Field

from app.api.api_v1.base_dto import UserBase
from app.api.api_v1.company.dto import CompanyRead
from app.core.database.models.enums.user_role import UserRole


# class UserBase(schemas.BaseModel):
#     first_name: str
#     last_name: str
#     phone: None | str  = Field(default=None)


class UserRead(UserBase, schemas.BaseUser[int]):
    role: UserRole
    company: CompanyRead | None


class UserCreate(UserBase, schemas.BaseUserCreate):
    invite_code: str | None = Field(default=None)


class UserUpdate(schemas.BaseUserUpdate):
    pass


