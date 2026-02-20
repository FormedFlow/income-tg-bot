from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models import Currency, ExchangeRate


async def get_exchange_rate(
        session: AsyncSession,
        currency_from: Currency,
        currency_to: Currency,
        date: date
):
    stmt = (select(ExchangeRate)
            .where(ExchangeRate.base_currency == currency_from)
            .where(ExchangeRate.change_currency == currency_to)
            .where(ExchangeRate.date == date))
    result = await session.scalar(stmt)
    return result