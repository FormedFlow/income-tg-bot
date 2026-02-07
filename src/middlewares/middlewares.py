from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker
from core.models import User
from sqlalchemy import select


class DBSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    async def __call__(self, handler, event, data):
        async with self.session_pool() as session:
            data['session'] = session
            result = await handler(event, data)
            return result
        

class UserMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    async def __call__(self, handler, event, data):
        async with self.session_pool() as session:
            tg_user_id = data['event_context'].user.id
            stmt = select(User).where(User.tg_user_id == tg_user_id)
            user = await session.scalar(stmt)
            data['user'] = user
            result = await handler(event, data)
            return result
            