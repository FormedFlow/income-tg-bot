from core.models import *
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from core.database import async_seshmaker
from datetime import datetime
from decimal import Decimal


async def get_all_categories(session: AsyncSession):
    stmt = select(Category)
    result = await session.scalars(stmt)
    return result


# async def get_expense_categories(session: AsyncSession):
#     stmt = select(Category).where(Category.is_income == False)
#     result = await session.scalars(stmt)
#     return result


# async def get_income_categories(session: AsyncSession):
#     stmt = select(Category).where(Category.is_income == True)
#     result = await session.scalars(stmt)
#     return result


async def get_user_categories_by_is_income(session: AsyncSession, user_id: int, is_income: bool):
    stmt = (select(Category)
            .join(user_category)
            .where(user_category.c.user_id == user_id)
            .where(Category.is_income == is_income))
    result = await session.scalars(stmt)
    return result


async def create_transaction(
        session: AsyncSession,
        user_id: int,
        category_id: int,
        currency_id: int,
        date: datetime,
        is_income: bool,
        amount: Decimal,
        message: str
) -> Transaction:
    transaction = Transaction(
        user_id=user_id,
        category_id=category_id,
        currency_id=currency_id,
        date=date,
        is_income=is_income,
        amount=amount,
        message=message
    )
    session.add(transaction)
    await session.commit()
    return transaction


async def main():
    async with async_seshmaker() as session:
        result = await get_all_categories(session)
        for category in result:
            print(category.name, category.emoji)



if __name__ == '__main__':
    asyncio.run(main())