from aiogram.fsm.state import StatesGroup, State

class AdminReply(StatesGroup):
    waiting_text = State()
