from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from keyboards.reg_keyboards import name_confirm_kb, RegConfirmCbData

from services.registration import get_user_by_tg_id, insert_user


router = Router()


class Registration(StatesGroup):
    waiting_for_name = State()
    waiting_for_name_confirm = State()
    registered = State()


async def reset_reg_state(message: Message, state: FSMContext):
    await state.set_state(Registration.waiting_for_name)
    await message.answer('Как к тебе можно обращаться?')


@router.message(CommandStart())
async def start(message: Message, state: FSMContext, session: AsyncSession):
    try:
        print(f'BOT ID = {message.bot.id}, USER ID = {message.from_user.id}')
        user = await get_user_by_tg_id(message.from_user.id, session)
        print(user)
    except Exception as e:
        print('Exception is thrown while fetching user from db: {e.value}')
    if user:
        await message.answer('Браток ты уже зареган!')
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
async def accept_name(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    name = data.get('name')
    try:
        print(f'USER ID = {callback.from_user.id}')
        user = await insert_user(session, callback.from_user.id, name)
        print(f'user = {user}')
    except Exception as e:
        print(f'Exception is thrown while inserting user: {e}')
    print('##########'*5)
    # print(f'user = {user}')
    await callback.answer()
    # await state.set_state(Registration.registered)
    await state.clear()
    await callback.message.answer(text=f'Ну чтож, {name}, продолжим')
 

@router.callback_query(RegConfirmCbData.filter())
async def random_press(callback: CallbackQuery):
    await callback.answer()