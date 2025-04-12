from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup

from handlers.fsm_registration import (
    CommandRegistration,
    SoloRegistration
    )
from keyboards.keyboards import (
    main_keyboard,
    main_game_keyboard,
    main_team_or_solo_keyboard
    )
from lexicon.lexicon import LEXICON

router = Router()

@router.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.reply(
        LEXICON["/start"],
        reply_markup=main_keyboard
        )

@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.reply(
        LEXICON["/help"], 
        reply_markup=main_keyboard
        )

@router.message(F.text == LEXICON["register_button"])
@router.message(Command(commands="register"))
async def process_register_command(message: Message):
    await message.reply(
        LEXICON["/register"], 
        reply_markup=main_team_or_solo_keyboard
        )

@router.message(F.text == LEXICON["solo_button"])
async def prcess_solo_registration(message: Message):
    await message.answer(
        "Выбрана регистрация в соло. \n\n" \
        "В какой дисциплине вы хотите принять участие?",
        reply_markup=main_game_keyboard
        )

@router.message(F.text == LEXICON["team_button"])
async def prcess_team_registration(message: Message):
     await message.answer(
        "Выбрана регистрация команды. \n\n" \
        "В какой дисциплине вы хотите принять участие?",
        reply_markup=main_game_keyboard
        )

@router.message(F.text == LEXICON["cs_choose_button"])
async def prcess_cs_registration(message: Message):
    await message.answer("Введите название команды: ")
    await state.set_state(CommandRegistration.fill_command_name)

@router.message(F.text == LEXICON["dota_choose_button"])
async def prcess_dota_registration(message: Message):
    await message.answer("Тут будет реализация регистрации Дота")

@router.message(F.text == LEXICON["back_button"])
async def prcess_back_registration(message: Message):
    await message.answer("Тут будет реализация шага назад")