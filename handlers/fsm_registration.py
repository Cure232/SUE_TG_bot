from aiogram.fsm.state import State, StatesGroup

class CommandRegistration(StatesGroup):
    fill_command_name = State()
    fill_name = State()
    fill_group = State()
    fill_photo = State()
    fill_info = State()


class SoloRegistration(StatesGroup):
    fill_name = State()
    fill_group = State()
    fill_photo = State()
    fill_info = State()
