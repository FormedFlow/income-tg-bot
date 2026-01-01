from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class RegConfirmCbData(CallbackData, prefix='reg-confirm'):
    confirm: bool


name_confirm_kb = InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(text='Да', callback_data=RegConfirmCbData(confirm=True).pack()), 
         InlineKeyboardButton(text='Нет', callback_data=RegConfirmCbData(confirm=False).pack())]
    ]
)