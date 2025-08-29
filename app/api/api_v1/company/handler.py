from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status, Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.api.api_v1.base_dto import AddUserRequest, RemoveUserRequest
from app.api.api_v1.company.dto import CompanyCreate, CompanyRead, CompanyUpdate, CompanyBase
from app.core import settings
from app.core.authentication.methods import verify_api_key, http_bearer
from app.core.services.company import CompanyService
from app.core.services.permissions import CheckPermission


router = APIRouter(
    prefix=settings.api.v1.company,
    tags=["Company"],
)


@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    response_model=CompanyCreate,
)
@inject
async def create_company(
        company_data: CompanyCreate,
        perm: FromDishka[CheckPermission],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
        service: FromDishka[CompanyService],
):
    await perm.check_is_admin_or_superuser(
        token=credentials.credentials,
        only_admin=True,
    )
    return await service.create_company(company_data=company_data)


@router.get(
    path="/companies/{id}",
    status_code=status.HTTP_200_OK,
    response_model=CompanyRead,
)
@inject
async def get_company_by_id(
        company_id: int,
        service: FromDishka[CompanyService],
):
    company = await service.get_by_id(company_id=company_id)
    return company


@router.get(
    "/service/{company_id}",
    response_model=CompanyBase,
    # dependencies=[Depends(verify_api_key)]
)
@inject
async def get_company_by_id_service(
        company_id: int,
        service: FromDishka[CompanyService],
):
    return await service.get_by_id(company_id=company_id)


@router.patch(
    path="/companies/{id}",
    status_code=status.HTTP_200_OK,
    response_model=CompanyRead,
)
@inject
async def update_company(
        company_id: int,
        user_data: CompanyUpdate,
        perm: FromDishka[CheckPermission],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
        service: FromDishka[CompanyService]
):
    await perm.check_is_admin_or_superuser(
        token=credentials.credentials,
        company_id=company_id,
    )
    return await service.update(company_id=company_id, user_data=user_data)


@router.post(
    path="/{company_id}/users",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def add_user_to_company(
    company_id: int,
    user_data: AddUserRequest,
    perm: FromDishka[CheckPermission],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
    service: FromDishka[CompanyService],

):
    await perm.check_is_admin_or_superuser(
        token=credentials.credentials,
        company_id=company_id,
    )
    return await service.add_user_in_company(
        company_id=company_id,
        user_id=user_data.user_id,
        role=user_data.role,
    )


@router.delete(
    path="/{company_id}/users",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def del_user_from_company(
    company_id: int,
    user_data: RemoveUserRequest,
    perm: FromDishka[CheckPermission],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
    service: FromDishka[CompanyService],
):
    await perm.check_is_admin_or_superuser(
        token=credentials.credentials,
        company_id=company_id,
    )
    return await service.del_user_from_company(
        company_id=company_id,
        user_id=user_data.user_id,
    )