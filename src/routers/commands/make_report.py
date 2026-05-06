from aiogram import Router
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.types import BufferedInputFile
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.report_keyboards import report_type_keyboard, ReportTypeCbData
from keyboards.report_keyboards import report_time_keyboard, ReportTimeCbData
from states.report_state import ReportState
from services.report import get_grouped_transactions, make_pie_chart
from core.models import User


router = Router()


@router.message(Command('make_report'))
async def handle_make_report(
    message: Message,
    state: FSMContext
):
    await state.set_state(ReportState.waiting_for_type)
    await message.answer(
        text='Выбери направление отчёта:',
        reply_markup=report_type_keyboard
    )
    

@router.callback_query(ReportTypeCbData.filter(), ReportState.waiting_for_type)
async def handle_report_type(
    callback: CallbackQuery,
    callback_data: ReportTypeCbData,
    state: FSMContext
):
    await state.update_data(type=callback_data.type)
    await state.set_state(ReportState.waiting_for_time)
    await callback.answer()
    await callback.message.answer(
        text='Выбери период:',
        reply_markup=report_time_keyboard
    )


@router.callback_query(ReportTimeCbData.filter(F.time == 'arbitrary'), ReportState.waiting_for_time)
async def handle_report_arbitrary_time(
    callback: CallbackQuery,
    callback_data: ReportTimeCbData,
    state: FSMContext
):
    await state.set_state(ReportState.waiting_for_start_date)
    await callback.answer()
    await callback.message.answer(text='Введите начальную дату в формате dd.mm.yyyy. Например, 01.02.2026')


@router.message(ReportState.waiting_for_start_date)
async def handle_start_date(
    message: Message,
    state: FSMContext
):
    try:
        start_date = date.strptime(message.text, '%d.%m.%Y')
    except ValueError as e:
        await message.answer('Вы ввели неверную дату, пожалуйста, введите начальную дату повторно')
    else:
        await state.update_data(start_date=start_date)
        await state.set_state(ReportState.waiting_for_end_date)
        await message.answer(text='Теперь введите конечную дату:')


@router.message(ReportState.waiting_for_end_date)
async def handle_end_date(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    user: User
):
    data = await state.get_data()
    start_date = data['start_date']
    report_type = data['type']
    try:
        end_date = date.strptime(message.text, '%d.%m.%Y')
    except ValueError as e:
        await message.answer(text='Вы ввели неверную дату, пожалуйста, введите конечную дату повторно')
    else:
        await state.update_data(end_date=end_date)
        await message.answer(text='Идёт подготовка отчёта...')
        groups = await get_grouped_transactions(
            session=session,
            user=user,
            date_start=start_date,
            date_end=end_date,
            report_type=report_type
        )
        if groups == []:
            text_expenses = 'За указанный период не было совершено покупок.'
            text_incomes = 'За указанный период не было добавлено доходов.'
            text_answer = text_expenses if report_type == 'expenses' else text_incomes
            await message.answer(text_answer)
        else:
            bio = make_pie_chart(groups)
            file = BufferedInputFile(file=bio.read(), filename='plot.png')
            bio.close()
            await message.answer_photo(file)
        await state.clear()


    # реализовать формирование отчёта!!!!
    
    

@router.callback_query(ReportTimeCbData.filter(), ReportState.waiting_for_time)
async def handle_report_time(
    callback: CallbackQuery,
    callback_data: ReportTimeCbData,
    state: FSMContext,
    session: AsyncSession,
    user: User
):
    data = await state.get_data()
    # print(f'DATA = {data}')
    report_type = data['type']
    date_end = date.today() + timedelta(days=1)
    interval = callback_data.time
    delta = None
    match interval:
        case 'week':
            delta = timedelta(weeks=1)
        case 'two-weeks':
            delta = timedelta(weeks=2)
        case 'month':
            delta = timedelta(days=30)
        case 'year':
            delta = timedelta(days=365)
    date_start = date_end - delta
    groups = await get_grouped_transactions(
        session=session,
        user=user,
        date_start=date_start,
        date_end=date_end,
        report_type=report_type
    )
    print(f'GROUPS = {groups}')
    bio = make_pie_chart(groups)
    file = BufferedInputFile(file=bio.read(), filename='plot.png')
    bio.close()
    await state.clear()
    await callback.answer()
    await callback.message.answer_photo(file)

    

