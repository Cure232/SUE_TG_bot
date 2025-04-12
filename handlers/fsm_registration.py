from aiogram.fsm.state import State, StatesGroup

class TeamRegistration(StatesGroup):
    fill_team_name = State()
    fill_name = State()
    fill_group = State()
    fill_link = State()
    fill_photo = State()
    team_counter = State()

class SoloRegistration(StatesGroup):
    fill_name = State()
    fill_group = State()
    fill_link = State()
    fill_photo = State()
