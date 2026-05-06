from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, between, func
from datetime import date
import asyncio
import matplotlib.pyplot as plt
from decimal import Decimal
from io import BytesIO

from core.models import Transaction, User, Category
from core.database import async_seshmaker


async def get_grouped_transactions(
    session: AsyncSession,
    user: User,
    date_start: date,
    date_end: date,
    report_type: str
):
    stmt = (select(Category.name, func.sum(Transaction.amount))
            .join(Transaction)
            .where(Transaction.user_id == user.user_id)
            .where(between(Transaction.date, date_start, date_end))
            .group_by(Transaction.category_id))
    if report_type in ('expenses', 'incomes'):
        is_income = (report_type == 'incomes')
        stmt = stmt.where(Transaction.is_income == is_income)
    result = await session.execute(stmt)
    return result.all()


def make_pie_chart(groups: tuple[str, Decimal]):
    fig, ax = plt.subplots(figsize=(2, 2), subplot_kw=dict(aspect='equal'))
    data = [round(float(num), 2) for name, num in groups]
    names = [name for name, num in groups]
    def func(pct, values):
        abs_value = int(pct/100 * sum(data))
        return f'{pct:.1f}%\n{abs_value:d}р' if pct > 1 else f'{pct:.1f}%'
    wedges, texts, autotexts = ax.pie(
        data, autopct=lambda pct: func(pct, data),
        pctdistance=1.5,
        textprops=dict(color='black'),
        wedgeprops={'linewidth': 0.5,
                    'edgecolor': 'black'}
    )
    ax.legend(wedges, [name for name, num in groups],
            title="Категории",
            loc="center left",
            bbox_to_anchor=(1.5, 0, 0.5, 1),
            prop={'size': 6},
            title_fontproperties={'size': 7})
    plt.setp(autotexts, size=5, weight='bold')
    bio = BytesIO()
    fig.savefig(bio, format='png', bbox_inches='tight', dpi=300)
    # plt.show()
    plt.close()
    bio.seek(0)
    return bio


def make_pie_test(groups: tuple[str, Decimal]):
    fig, ax = plt.subplots(figsize=(2, 2), subplot_kw=dict(aspect='equal'))
    data = [round(float(num), 2) for name, num in groups]
    names = [name for name, num in groups]
    print('########################' * 3)
    print(data, names)
    def func(pct, data):
        abs_value = int(pct/100 * sum(data))
        return f'{pct:.1f}%\n{abs_value:d}р'
    wedges, texts, autotexts = ax.pie(
        data, autopct=lambda pct: func(pct, data),
        pctdistance=1.4,
        textprops=dict(color='black')
    )
    ax.legend(wedges, [name for name, num in groups],
            title="Категории",
            loc="center left",
            bbox_to_anchor=(1.5, 0, 0.5, 1),
            prop={'size': 6},
            title_fontproperties={'size': 7})
    plt.setp(autotexts, size=5, weight='bold')
    plt.show()
    plt.close()


async def main():
    async with async_seshmaker() as session:
        date_start, date_end = date(2026, 2, 20), date(2026, 3, 1)
        user_stmt = select(User).where(User.user_id == 4)
        user = await session.scalar(user_stmt)
        groups = await get_grouped_transactions(
            session=session,
            user=user,
            date_start=date_start,
            date_end=date_end,
            report_type='expenses'
        )
        # for trans in groups:
        #     print(f'transaction_obj: {trans}')
    # bio = make_pie_chart(groups)
    # print(type(bio))
    # make_pie_test(groups)
    # print(type(groups))



if __name__ == '__main__':
    asyncio.run(main())