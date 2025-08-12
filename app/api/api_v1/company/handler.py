from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status, Request

from app.api.api_v1.company.dto import CompanyCreate, CompanyRead
from app.core import settings
from app.core.services.company import CompanyService

router = APIRouter(
    prefix=settings.api.v1.company,
    tags=["Company"],
)


@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    response_model=CompanyRead,
)
@inject
async def user_register(
        company_data: CompanyCreate,
        request: Request,
        service: FromDishka[CompanyService],
):
    return await service.create_company(request=request, company_data=company_data)

