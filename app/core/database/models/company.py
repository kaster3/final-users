import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.models.base import Base
from app.core.database.models.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .user import User
    from .department import Department


class Company(Base, IntIdPkMixin):

    name: Mapped[str] = mapped_column(String(100), unique=True)
    invite_code: Mapped[str] = mapped_column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    # created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Связи
    users: Mapped[list["User"]] = relationship(back_populates="company", lazy="joined")
    departments: Mapped[list["Department"]] = relationship(back_populates="company")