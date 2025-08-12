from app.api.api_v1.company.dto import CompanyCreate
from app.core.database.models import Company
from app.core.interfaces.company import IDBCompanyRepository


class CompanyService:
    def __init__(
            self,
            compony_repository: IDBCompanyRepository,
    ) -> None:
        self.company_repository = compony_repository

    async def create_company(
            self,
            company_data: CompanyCreate,
    ) -> Company:
        # todo проврку на админа
        company = await self.company_repository.create_company(company_data=company_data)
        return company
