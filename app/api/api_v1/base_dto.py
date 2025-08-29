from fastapi_users import schemas
from pydantic import Field, BaseModel

from app.core.database.models.enums.user_role import UserRole


class UserBase(schemas.BaseModel):
    first_name: str
    last_name: str
    phone: None | str  = Field(default=None)


class CompanyUserRead(UserBase, schemas.BaseUser[int]):
    role: str


class AddUserRequest(BaseModel):
    user_id: int
    role: UserRole = UserRole.MEMBER

class RemoveUserRequest(BaseModel):
    user_id: int