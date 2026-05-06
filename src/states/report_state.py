from aiogram.fsm.state import StatesGroup, State


class ReportState(StatesGroup):
    waiting_for_type = State()
    waiting_for_time = State()
    waiting_for_start_date = State()
    waiting_for_end_date = State()
    waiting_for_report = State()