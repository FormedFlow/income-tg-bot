from datetime import datetime, date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Numeric, BigInteger, Integer, Date
from sqlalchemy import func
from sqlalchemy import Table, Column
from decimal import Decimal
from sqlalchemy import Enum
from sqlalchemy.ext.asyncio import AsyncSession
import enum

# from services.exchange_rates import get_exchange_rate


class Base(DeclarativeBase):
    pass


class RecurringRate(enum.Enum):
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    YEAR = 'year'


user_category = Table(
    'user_category',
    Base.metadata,
    Column('user_category_id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('user.user_id', ondelete='RESTRICT')),
    Column('category_id', ForeignKey('category.category_id', ondelete='RESTRICT'))
)


class User(Base):
    __tablename__ = 'user'

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    name: Mapped[str] = mapped_column(String(45), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    is_admin: Mapped[bool] = mapped_column(default=False)
    default_currency_id: Mapped[int] = mapped_column(ForeignKey("currency.currency_id"), nullable=True)
    display_currency_id: Mapped[int] = mapped_column(ForeignKey("currency.currency_id"), nullable=True)

    transactions: Mapped['Transaction'] = relationship(back_populates='user')
    recurring_transactions: Mapped['RecurringTransaction'] = relationship(back_populates='user')
    categories: Mapped['Category'] = relationship(secondary='user_category')


class Category(Base):
    __tablename__ = 'category'

    category_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(45), nullable=False)
    emoji: Mapped[str] = mapped_column(String(5), default=None, nullable=True)
    is_income: Mapped[bool] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


    # не вижу пока какого-то дельного применения этим отношениям
    # transactions: Mapped['Transaction'] = relationship(back_populates='category', cascade='all, delete, delete-orphan')
    # recurring_transactions: Mapped['RecurringTransaction'] = relationship('category', cascade='all, delete, delete-orphan')


class Currency(Base):
    __tablename__ = 'currency'

    currency_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(45), nullable=False)
    code: Mapped[str] = mapped_column(String(10))
    symbol: Mapped[str] = mapped_column(String(10))
    display_precision: Mapped[int] = mapped_column()


class Transaction(Base):
    __tablename__ = 'transaction'

    transaction_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id", ondelete='RESTRICT'), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.category_id", ondelete='RESTRICT'), nullable=False)
    currency_id: Mapped[int] = mapped_column(ForeignKey("currency.currency_id", ondelete='RESTRICT'), nullable=False)
    converted_currency_id: Mapped[int] = mapped_column(ForeignKey("currency.currency_id", ondelete='RESTRICT'), nullable=True)
    date: Mapped[datetime] = mapped_column(nullable=False)
    is_income: Mapped[bool] = mapped_column(default=False)
    message: Mapped[str] = mapped_column(String(45), default=None, nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(22, 10), nullable=False)
    amount_converted_first: Mapped[Decimal] = mapped_column(Numeric(22, 10), nullable=True)
    amount_converted_current: Mapped[Decimal] = mapped_column(Numeric(22, 10), nullable=True)
    exchange_rate_first_id: Mapped[int] = mapped_column(ForeignKey("exchange_rate.rate_id", ondelete='RESTRICT'), nullable=True)
    exchange_rate_current_id: Mapped[int] = mapped_column(ForeignKey("exchange_rate.rate_id", ondelete='RESTRICT'), nullable=True)
    last_recalculated_at: Mapped[datetime] = mapped_column(default=None, nullable=True)

    user: Mapped['User'] = relationship(back_populates='transactions')
    category: Mapped['Category'] = relationship(lazy='selectin')
    og_currency: Mapped['Currency'] = relationship(lazy='selectin', foreign_keys="Transaction.currency_id")
    re_currency: Mapped['Currency'] = relationship(lazy='selectin', foreign_keys="Transaction.converted_currency_id")


    def __str__(self):
        return f'Transaction instance, transaction id={self.transaction_id}, amount={self.amount}, date={self.date}'


    async def convert_to(
            self,
            session: AsyncSession,
            currency: Currency
    ):
        # rate_date = date.today()
        # rate = None
        # while rate is None:
        #     exchane_rate = await get_exchange_rate(
        #         session,
        #         self.currency_id, 
        #         currency.currency_id, 
        #         rate_date
        #     )
        #     rate_date = rate_date.replace(day=date.today().day - 1)
        # exchange_rate = rate.exchange_rate
        # self.amount_converted
        pass


class RecurringTransaction(Base):
    __tablename__ = 'recurring_transaction'

    transaction_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='RESTRICT'), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.category_id', ondelete='RESTRICT'), nullable=False)
    date_added_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    amount: Mapped[Decimal] = mapped_column(Numeric(22, 10), nullable=False)
    currency_id: Mapped[int] = mapped_column(ForeignKey("currency.currency_id", ondelete='RESTRICT'), nullable=False)
    amount_converted_first: Mapped[Decimal] = mapped_column(Numeric(22, 10))
    amount_converted_current: Mapped[Decimal] = mapped_column(Numeric(22, 10))
    exchange_rate: Mapped[Decimal] = mapped_column(Numeric(24, 12))
    rate_source_first: Mapped[str] = mapped_column(String(45))
    rate_source_current: Mapped[str] = mapped_column(String(45))
    interval_type: Mapped[RecurringRate] = mapped_column(Enum(RecurringRate, validate_strings=True))
    last_recalculated_at: Mapped[datetime] = mapped_column(default=None)

    user: Mapped['User'] = relationship()
    category: Mapped['Category'] = relationship()


class ExchangeRate(Base):
    __tablename__ = 'exchange_rate'

    rate_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    base_currency: Mapped['Currency'] = mapped_column(ForeignKey("currency.currency_id", ondelete='RESTRICT'), nullable=True)
    change_currency: Mapped['Currency'] = mapped_column(ForeignKey("currency.currency_id", ondelete='RESTRICT'), nullable=True)
    date: Mapped[date] = mapped_column(Date)
    exchange_rate: Mapped[Decimal] = mapped_column(Numeric(24, 12), nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(default=datetime.now(), nullable=True)
    
