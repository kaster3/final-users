from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.models.base import Base
from app.core.database.models.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .company import Company

class Department(Base, IntIdPkMixin):

    name: Mapped[str] = mapped_column(String(100))

    # Иерархия (родительское подразделение)
    parent_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("departments.id"),
        nullable=True
    )

    # Связь с компанией
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"))
    company: Mapped["Company"] = relationship(back_populates="departments")