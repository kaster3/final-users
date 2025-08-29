from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from app.api.api_v1.base_dto import CompanyUserRead


class CompanyBase(BaseModel):
    name: str = Field(..., max_length=100)

class CompanyRead(CompanyBase):
    id: int
    users: list[CompanyUserRead]

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    pass