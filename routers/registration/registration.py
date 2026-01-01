from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.methods.send_message import SendMessage
from keyboards.reg_keyboards import name_confirm_kb, RegConfirmCbData


router = Router()

class Registration(StatesGroup):
    waiting_for_name = State()
    waiting_for_name_confirm = State()
    registered = State()


async def reset_reg_state(message: Message, state: FSMContext):
    await state.set_state(Registration.waiting_for_name)
    await message.answer('Как к тебе можно обращаться?')


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state == Registration.registered.state:
        await message.answer('Браток, ты уже зареган')
        return None
    await message.answer('Привет!')
    await reset_reg_state(message, state)


@router.message(Registration.waiting_for_name, F.text)
async def check_name(message: Message, state:FSMContext):
    if message.text.strip() == '':
        await message.answer('Пожалуйста, введите корректное имя.')
    else:
        await message.answer(
            text=f'{message.text}, ok?',
            reply_markup=name_confirm_kb
        )
        await state.update_data(name=message.text)
        await state.set_state(Registration.waiting_for_name_confirm)


@router.callback_query(RegConfirmCbData.filter(F.confirm == False), Registration.waiting_for_name_confirm)
async def deny_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await reset_reg_state(callback.message, state)


@router.callback_query(RegConfirmCbData.filter(F.confirm == True), Registration.waiting_for_name_confirm)
async def accept_name(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get('name')
    await callback.answer()
    await state.set_state(Registration.registered)
    await callback.message.answer(text=f'Ну чтож, {name}, продолжим')
 

@router.callback_query(RegConfirmCbData.filter())
async def random_press(callback: CallbackQuery):
    await callback.answer()