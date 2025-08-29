from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyUserDatabase,
)

from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.models.base import Base
from app.core.database.models.mixins import IntIdPkMixin
from .enums.user_role import UserRole

if TYPE_CHECKING:
    from .company import Company


class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[int]):
    # Кастомные поля
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=True)
    # Роль внутри компании, есть еще роль от fastapi-users, она для админки
    role: Mapped[UserRole] = mapped_column(
        String(10),
        default=UserRole.MEMBER,
        nullable=False
    )
    company_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("companies.id"),
        nullable=True  # Пользователь может быть без компании
    )
    # Связи
    company: Mapped["Company"] = relationship(back_populates="users", lazy="joined")

    # Table args
    __table_args__ = (
        UniqueConstraint("phone", name="uq_user_phone"),
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)