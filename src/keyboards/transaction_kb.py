from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import StatesGroup, State

from services.transactions import get_all_categories
from core.models import Category
from decimal import Decimal
from datetime import datetime


class TransactionCbData(CallbackData, prefix='transaction-data'):
    category_id: int
    currency_id: int
    is_income: bool
    amount: float


def build_transaction_kb(
        categories: list[Category],
        currency_id: int,
        is_income: bool,
        amount: float
        ) -> InlineKeyboardBuilder:
    transaction_kb_builder = InlineKeyboardBuilder()
    for cat in categories:
        transaction_kb_builder.button(
            text=cat.emoji + ' ' + cat.name,
            callback_data=TransactionCbData(
                category_id=cat.category_id,
                currency_id=currency_id,
                is_income=is_income,
                amount=amount
            )
        )
    transaction_kb_builder.adjust(3)
    transaction_kb_builder.row(
        InlineKeyboardButton(text='➕ Добавить категорию',
                             callback_data='blank')
    )
    return transaction_kb_builder


