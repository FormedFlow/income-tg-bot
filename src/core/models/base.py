from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Numeric, BigInteger
from sqlalchemy import func
from decimal import Decimal
from sqlalchemy import Enum
import enum


class Base(DeclarativeBase):
    pass


class RecurringRate(enum.Enum):
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    YEAR = 'year'


class User(Base):
    __tablename__ = 'user'

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    name: Mapped[str] = mapped_column(String(45), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    is_admin: Mapped[bool] = mapped_column(default=False)

    transactions: Mapped['Transaction'] = relationship(back_populates='user')
    recurring_transactions: Mapped['RecurringTransaction'] = relationship(back_populates='user')


class Category(Base):
    __tablename__ = 'category'

    category_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(45), nullable=False)
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


class Transaction(Base):
    __tablename__ = 'transaction'

    transaction_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id", ondelete='RESTRICT'), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.category_id", ondelete='RESTRICT'), nullable=False)
    currency_id: Mapped[int] = mapped_column(ForeignKey("currency.currency_id", ondelete='RESTRICT'))
    date: Mapped[datetime] = mapped_column(nullable=False)
    is_income: Mapped[bool] = mapped_column(default=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(22, 10), nullable=False)
    amount_converted_first: Mapped[Decimal] = mapped_column(Numeric(22, 10))
    amount_converted_current: Mapped[Decimal] = mapped_column(Numeric(22, 10))
    exchange_rate_first: Mapped[Decimal] = mapped_column(Numeric(24, 12))
    exchange_rate_current: Mapped[Decimal] = mapped_column(Numeric(24, 12))
    rate_source_first: Mapped[str] = mapped_column(String(45))
    rate_source_current: Mapped[str] = mapped_column(String(45))
    last_recalculated_at: Mapped[datetime] = mapped_column(default=None)

    user: Mapped['User'] = relationship(back_populates='transactions')
    category: Mapped['Category'] = relationship()
    currency: Mapped['Currency'] = relationship()


class RecurringTransaction(Base):
    __tablename__ = 'recurring_transaction'

    transaction_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='RESTRICT'), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.category_id', ondelete='RESTRICT'), nullable=False)
    date_added_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    amount: Mapped[Decimal] = mapped_column(Numeric(22, 10), nullable=False)
    currency: Mapped[int] = mapped_column(ForeignKey("currency.currency_id", ondelete='RESTRICT'), nullable=False)
    amount_converted_first: Mapped[Decimal] = mapped_column(Numeric(22, 10))
    amount_converted_current: Mapped[Decimal] = mapped_column(Numeric(22, 10))
    exchange_rate: Mapped[Decimal] = mapped_column(Numeric(24, 12))
    rate_source_first: Mapped[str] = mapped_column(String(45))
    rate_source_current: Mapped[str] = mapped_column(String(45))
    interval_type: Mapped[RecurringRate] = mapped_column(Enum(RecurringRate, validate_strings=True))
    last_recalculated_at: Mapped[datetime] = mapped_column(default=None)

    user: Mapped['User'] = relationship()
    category: Mapped['Category'] = relationship()

