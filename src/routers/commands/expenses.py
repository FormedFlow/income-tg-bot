from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram import F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from decimal import Decimal

from core.models import User
from services.transactions import get_user_categories_by_is_income, create_transaction
from keyboards.transaction_kb import build_transaction_kb, TransactionCbData
from states.transaction_state import TransactionState


router = Router()


@router.message(F.text.regexp(r'^[-+]?[1-9]+[0-9]*'))
async def handle_transaction_start(message: Message, session: AsyncSession, user: User, state: FSMContext):
    is_income = False
    if message.text.startswith('+'):
        is_income = True
    text = message.text
    amount = float(text[1:] if text[0] in ('+', '-') else text)
    categories = await get_user_categories_by_is_income(
        session=session,
        user_id=user.user_id,
        is_income=is_income
    )
    transaction_kb = build_transaction_kb(
        categories=categories,
        currency_id=user.default_currency_id,
        is_income=is_income,
        amount=amount
    )
    await state.set_state(TransactionState.choosing_category)
    await message.answer(
        text='Выбери категорию',
        reply_markup=transaction_kb.as_markup()
    )


@router.callback_query(TransactionCbData.filter(), TransactionState.choosing_category)
async def handle_transaction_finish(
    callback: CallbackQuery,
    session: AsyncSession,
    callback_data: CallbackData,
    user: User,
    state: FSMContext
):
    if not user.default_currency_id == user.display_currency_id:
        return
    transaction = await create_transaction(
        session=session,
        user_id=user.user_id,
        category_id=callback_data.category_id,
        currency_id=callback_data.currency_id,
        date=datetime.now(),
        is_income=callback_data.is_income,
        amount=Decimal(callback_data.amount),
        message=None
    )
    print(transaction.transaction_id)
    await callback.answer()
    await state.clear()
    await callback.message.answer(text='Транзакция создана')


@router.callback_query(TransactionCbData.filter())
async def handle_random_category_press(callback: CallbackQuery):
    await callback.answer()