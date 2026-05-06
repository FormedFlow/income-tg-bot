from aiogram.fsm.state import StatesGroup, State


class TransactionState(StatesGroup):
    choosing_category = State()
    

class ShowCategoriesState(StatesGroup):
    choosing_is_income = State()
    choosing_category = State()


class PaginationState(StatesGroup):
    waiting_for_page_button_press = State()