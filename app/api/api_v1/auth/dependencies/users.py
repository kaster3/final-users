from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.db_helper import db_helper
from app.core.database.models.user import User


async def get_user_db(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)]
):
    yield User.get_db(session=session)