from dishka import Provider, Scope, provide
from fastapi_users.password import PasswordHelper

from app.core.repositories.company import SQLAlchemyCompanyRepository, IDBCompanyRepository
from app.core.repositories.user import IUserRepository, SQLAlchemyUserRepository
from app.core.services.company import CompanyService
from app.core.services.jwt import JWTHelper
from app.core.services.user import UserService


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    user_repo = provide(SQLAlchemyUserRepository, provides=IUserRepository)
    company_repo = provide(SQLAlchemyCompanyRepository, provides=IDBCompanyRepository)

    jwt_helper = provide(JWTHelper)

    company_service = provide(CompanyService)
    user_service = provide(UserService)


    @provide
    def get_password_helper(self) -> PasswordHelper:
        return PasswordHelper()