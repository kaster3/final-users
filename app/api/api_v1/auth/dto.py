from fastapi_users import schemas
from pydantic import Field


class UserBase(schemas.BaseModel):
    first_name: str
    last_name: str
    phone: str = Field(default="")


class UserRead(UserBase, schemas.BaseUser[int]):
    pass

class UserCreate(UserBase, schemas.BaseUserCreate):
    invite_code: str = Field(default="")


class UserUpdate(schemas.BaseUserUpdate):
    pass