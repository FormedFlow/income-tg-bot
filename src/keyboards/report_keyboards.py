from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class ReportTypeCbData(CallbackData, prefix='report-type-cb'):
    type: str


class ReportTimeCbData(CallbackData, prefix='report-time-cb'):
    time: str


report_type_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Расходы', callback_data=ReportTypeCbData(type='expenses').pack()),
         InlineKeyboardButton(text='Доходы', callback_data=ReportTypeCbData(type='incomes').pack()),
         InlineKeyboardButton(text='Всё вместе', callback_data=ReportTypeCbData(type='all').pack())]
    ]
)


report_time_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='За месяц', callback_data=ReportTimeCbData(time='month').pack()),
         InlineKeyboardButton(text='За две недели', callback_data=ReportTimeCbData(time='two-weeks').pack()),
         InlineKeyboardButton(text='За неделю', callback_data=ReportTimeCbData(time='week').pack()),
         InlineKeyboardButton(text='За год', callback_data=ReportTimeCbData(time='year').pack())],

        [InlineKeyboardButton(text='Произвольный период', callback_data=ReportTimeCbData(time='arbitrary').pack())]
    ]
)