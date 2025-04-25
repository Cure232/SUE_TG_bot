from aiogram.fsm.state import State, StatesGroup

class RegistrationSoloFSM(StatesGroup):
    fill_name = State()
    fill_group = State()
    fill_steam_lnk = State()
    fill_photo = State()
    fill_game = State()
    team_or_solo = State()
    fill_team_name = State()

class RegistrationTeamFSM(StatesGroup):
    fill_name = State()
    fill_group = State()
    fill_steam_lnk = State()
    fill_photo = State()
    fill_number = State()