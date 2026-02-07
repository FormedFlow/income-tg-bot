from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.models import Category


class IsIncomeCbData(CallbackData, prefix='is-income-data'):
    is_income: bool


class CategoryCbData(CallbackData, prefix='category-cb-data'):
    category_id: int


class PaginationCbData(CallbackData, prefix='pagination-cb-data'):
    active_page_num: int


is_income_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='💹 Доходы', callback_data=IsIncomeCbData(is_income=True).pack()),
         InlineKeyboardButton(text='🔻 Расходы', callback_data=IsIncomeCbData(is_income=False).pack())]
    ]
)


def build_category_keyboard(categories: list[Category]):
    category_keyboard_builder = InlineKeyboardBuilder()
    for cat in categories:
        category_keyboard_builder.button(
            text=cat.emoji + ' ' + cat.name,
            callback_data=CategoryCbData(category_id=cat.category_id).pack()
        )
    category_keyboard_builder.adjust(3)
    category_keyboard_builder.row(
        InlineKeyboardButton(text='➕ Добавить категорию', callback_data='blank')
    )
    return category_keyboard_builder


def build_pagination_keyboard(active_page: int, total_pages: int):
    pagination_builder = InlineKeyboardBuilder()
    if active_page != 1:
        pagination_builder.button(
            text='«1',
            callback_data=PaginationCbData(active_page_num=1).pack()
        )
    if active_page not in (1, 2):
        pagination_builder.button(
            text=f'‹{active_page-1}',
            callback_data=PaginationCbData(active_page_num=active_page-1).pack()
        )
    pagination_builder.button(
        text=str(active_page),
        callback_data='current_page'
    )
    if active_page != total_pages:
        pagination_builder.button(
            text=f'{total_pages}»',
            callback_data=PaginationCbData(active_page_num=total_pages).pack()
        )
    if total_pages - active_page >= 2:
        pagination_builder.button(
            text=f'{active_page+1}›',
            callback_data=PaginationCbData(active_page_num=active_page+1).pack()
        )
    pagination_builder.adjust(5)
    return pagination_builder