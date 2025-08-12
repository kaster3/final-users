from pydantic import Field, BaseModel


class CompanyBase(BaseModel):
    pass

class CompanyRead(CompanyBase):
    pass

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    pass