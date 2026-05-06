from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Category, Transaction, Currency
from core.database import async_seshmaker
import asyncio


async def get_user_transactions_by_category_id(session: AsyncSession, user_id, category_id):
    stmt = (select(Transaction)
            .where(Transaction.category_id == category_id)
            .where(Transaction.user_id == user_id))
    result = await session.scalars(stmt)
    return result


async def get_user_transactions_currency_by_caregory_id(
        session: AsyncSession,
        user_id: int,
        category_id: int,
        page: int = 1,
        per_page: int = 5
):
    total_stmt = (select(func.count(Transaction.transaction_id))
                          .where(Transaction.user_id == user_id)
                          .where(Transaction.category_id == category_id))
    total_transactions = await session.scalar(total_stmt)
    offset = (page - 1) * per_page
    trans_stmt = (select(Transaction)
                  .where(Transaction.user_id == user_id)
                  .where(Transaction.category_id == category_id)
                  .order_by(Transaction.date.desc())
                  .offset(offset)
                  .limit(per_page))
    transactions = await session.scalars(trans_stmt)
    return (transactions, total_transactions)


def format_category_transactions(num: int, 
                                 entry: Transaction):
    dt, amount = entry.date, entry.amount
    amount_emoji = '📈' if entry.is_income else '📉'
    clock, calendar = '🕐', '🗓'

    precision, symbol = entry.og_currency.display_precision, entry.og_currency.symbol
    trans_str = (f'{num+1}. {dt.strftime("%A").capitalize()}\n'+
                 f'{calendar} {dt.strftime("%d.%m.%y")}\n'+
                 f'{clock} {dt.strftime("%H:%M")}\n'+
                 f'{amount_emoji} {amount:.{precision}f}{symbol}\n')
    return trans_str


async def main():
    async with async_seshmaker() as session:
        transactions, total = await get_user_transactions_currency_by_caregory_id(
            session=session,
            user_id=4,
            category_id=3
        )
        print(transactions)
        print(total)


# if __name__ == '__main__':
#     asyncio.run(main())