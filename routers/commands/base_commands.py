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


router = Router()


class Registration(StatesGroup):
    waiting_for_name = State()
    confirming_name = State()


class RegistrationButtonData(CallbackData, prefix='registration-button-data'):
    response: bool


async def start_registration(message: Message, state: FSMContext):
    await state.set_state(Registration.waiting_for_name)
    await message.answer('Привет, как к тебе можно обращаться?')


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await start_registration(message, state)


@router.message(Registration.waiting_for_name, F.text)
async def get_name(message: Message, state: FSMContext):
    markup = InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(text='Да', callback_data=RegistrationButtonData(response=True).pack()), 
         InlineKeyboardButton(text='Нет', callback_data=RegistrationButtonData(response=False).pack())]
    ])

    if message.text is None or message.text.strip() == '':
        await message.answer('Так чё с именем?')
    else:
        await state.update_data(name=message.text)
        await state.set_state(Registration.confirming_name)
        await message.answer(
            text=f'{message.text}, ok?',
            reply_markup=markup
        )


@router.callback_query(RegistrationButtonData.filter(F.response == True), Registration.confirming_name)
async def handle_yes_button(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.answer('thats crazy')


@router.callback_query(RegistrationButtonData.filter(F.response == False), Registration.confirming_name)
async def handle_no_button(callback_query:CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.answer()
    await start_registration(callback_query.message, state)


@router.callback_query(RegistrationButtonData.filter())
async def handle_button_error(callback_query: CallbackQuery):
    await callback_query.answer('Выбор невозможен')


