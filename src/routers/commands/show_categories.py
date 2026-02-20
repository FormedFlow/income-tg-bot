from aiogram import Router
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.filters.callback_data import CallbackData
from sqlalchemy.ext.asyncio import AsyncSession
import math

from core.models import User
from services.transactions import get_user_categories_by_is_income
from services.categories import get_user_transactions_currency_by_caregory_id
from services.categories import format_category_transactions
from states.transaction_state import ShowCategoriesState
from states.transaction_state import PaginationState
from keyboards.category_kb import is_income_keyboard, IsIncomeCbData
from keyboards.category_kb import build_category_keyboard, CategoryCbData
from keyboards.category_kb import build_pagination_keyboard, PaginationCbData


router = Router()


@router.message(Command('help'))
async def help_handler(message: Message):
    pass


@router.message(Command('show_categories'))
async def show_categories_handle(message: Message, state: FSMContext):
    await state.set_state(ShowCategoriesState.choosing_is_income)
    await message.answer(
        text='Доходы или расходы?',
        reply_markup=is_income_keyboard
    )


@router.callback_query(IsIncomeCbData.filter(), ShowCategoriesState.choosing_is_income)
async def handle_is_income_callback(callback: CallbackQuery, 
                                     callback_data: CallbackData, 
                                     session: AsyncSession,
                                     user: User,
                                     state: FSMContext):
    await state.set_state(ShowCategoriesState.choosing_category)
    categories = await get_user_categories_by_is_income(session=session,
                                                        user_id=user.user_id,
                                                        is_income=callback_data.is_income)
    await callback.answer()
    await callback.message.answer(
        text='Выбери категорию, чтобы посмотреть траты по ней:',
        reply_markup=build_category_keyboard(categories).as_markup()
    )


@router.callback_query(CategoryCbData.filter(), ShowCategoriesState.choosing_category)
async def handle_category_callback(
    callback: CallbackQuery,
    callback_data: CallbackData,
    state: FSMContext,
    session: AsyncSession,
    user: User
):
    transactions, total = await get_user_transactions_currency_by_caregory_id(
        session=session,
        user_id=User.user_id,
        category_id=callback_data.category_id,
        page=1
    )
    active_page, per_page = 1, 5
    total_pages = math.ceil(total/per_page)
    await state.set_state(PaginationState.waiting_for_page_button_press)
    await state.update_data(
        total_pages=total_pages,
        category_id=callback_data.category_id
    )

    pages_keyboard = build_pagination_keyboard(
        active_page=active_page,
        total_pages=total_pages
    )
    text = ''
    for num, trans in enumerate(transactions):
        text = text + format_category_transactions(num, trans) + '\n'
    await callback.answer()
    await callback.message.answer(
        text=text,
        reply_markup=pages_keyboard.as_markup()
    )
    

@router.callback_query(PaginationCbData.filter(), PaginationState.waiting_for_page_button_press)
async def handle_page_switch(
    callback: CallbackQuery,
    callback_data: CallbackData,
    state: FSMContext,
    session: AsyncSession,
    user: User
):
    data = await state.get_data()
    category_id = data['category_id']
    active_page, total_pages = callback_data.active_page_num, data['total_pages']
    pages_keyboard = build_pagination_keyboard(
        active_page=active_page,
        total_pages=total_pages
    )
    transactions, _ = await get_user_transactions_currency_by_caregory_id(
        session=session,
        user_id=user.user_id,
        category_id=category_id,
        page=active_page
    )
    text = ''
    for num, trans in enumerate(transactions):
        text = text + '\n' + format_category_transactions(num, trans)
    await callback.answer()
    await callback.message.answer(
        text=text,
        reply_markup=pages_keyboard.as_markup()
    )


@router.callback_query(F.data == 'current_page')
async def handle_active_page_click(callback: CallbackQuery):
    await callback.answer()