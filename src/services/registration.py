from sqlalchemy import select
from core.config import base_settings
from core.models import *


async def get_user_by_tg_id(tg_user_id, async_session):
    stmt = select(User).filter_by(tg_user_id=tg_user_id)
    result = await async_session.scalar(stmt)
    return result


async def insert_user(async_sesh, tg_user_id, name, is_admin=False):
    async with async_sesh.begin():
        user = User(
            tg_user_id=tg_user_id,
            name=name,
            is_admin=is_admin
        )
        async_sesh.add(user)
        await async_sesh.flush()
        await async_sesh.refresh(user)
        return user
