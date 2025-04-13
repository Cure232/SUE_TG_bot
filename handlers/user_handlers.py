from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from handlers.fsm_registration import RegistrationFSM
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

@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        "Вы прекратили процесс регистрации."
        )
    await state.clear()

@router.message(F.text == LEXICON["register_button"], StateFilter(default_state))
@router.message(Command(commands="register"))
async def process_register_command(message: Message, state: FSMContext):
    await state.set_state(RegistrationFSM.fill_name)
    await message.answer(
        "Начата регистрация на турнир. \n" 
        "\nНапишите ваше ФИО."
        )

@router.message(StateFilter(RegistrationFSM.fill_name), F.text.isalpha())
async def process_name_registration(message: Message, state: FSMContext):
    await state.update_data(fill_name=message.text)
    await state.set_state(RegistrationFSM.fill_group)
    await message.answer(
        "Данные сохранены. \n" 
        "\nВведите номер группы.  "
        )

@router.message(StateFilter(RegistrationFSM.fill_group))
async def process_group_registration(message: Message, state: FSMContext):
    await state.update_data(fill_group=message.text)
    await state.set_state(RegistrationFSM.fill_steam_lnk)
    await message.answer(
        "Данные сохранены. \n" 
        "\nВведите ссылку на STEAM. "
        )

@router.message(StateFilter(RegistrationFSM.fill_steam_lnk))
async def process_link_registration(message: Message, state: FSMContext):
    await state.update_data(fill_link=message.text)
    await state.set_state(RegistrationFSM.fill_photo)
    await message.answer(
        "Данные сохранены. \n" 
        "\nПрикрепите фотографию студенческого для верификации. "
        )

@router.message(StateFilter(RegistrationFSM.fill_photo), F.photo)
async def process_photo_registration(message: Message, state: FSMContext):
    first_photo = message.photo[0]

    await state.update_data(fill_photo=first_photo.file_id)
    await state.set_state(RegistrationFSM.fill_game)
    await message.answer(
        "Данные сохранены. \n" 
        "\nВыберите дисциплину для турнира",
        reply_markup=main_game_keyboard
    )

@router.message(F.text.in_({LEXICON["dota_game_button"], LEXICON["cs_game_button"]}), 
                StateFilter(RegistrationFSM.fill_game))
async def process_game_registration(message: Message, state: FSMContext):
    await state.update_data(fill_game=message.text)
    await state.set_state(RegistrationFSM.team_or_solo)
    await message.answer(
        f"Выбрана дисциплина {message.text}\n" 
        "\nУ вас есть команда?",
        reply_markup=main_team_or_solo_keyboard
        )

@router.message(F.text == LEXICON["team_button"], StateFilter(RegistrationFSM.team_or_solo))
async def process_team_registration(message: Message, state: FSMContext):
    await state.set_state(RegistrationFSM.fill_team_name)
    await message.answer(
        "\nВведите название вашей команды"
        )

@router.message(F.text == LEXICON["solo_button"], StateFilter(RegistrationFSM.team_or_solo))
async def process_solo_registration(message: Message, state: FSMContext):
    await message.answer("Регистрация завершена!")
    await state.clear()

@router.message(StateFilter(RegistrationFSM.fill_team_name))
async def process_team_name_registration(message: Message, state: FSMContext):
    print("dkwodkwd")
    await state.update_data(fill_team_name=message.text)
    await state.set_state(RegistrationFSM.add_teammate)
    await state.update_data(add_teammate=[])
    await message.answer(
        "\nТеперь поочередно введите данные других игроков."
        )

@router.message(F.text == LEXICON["back_button"])
async def prcess_back_registration(message: Message):
    await message.answer("Тут будет реализация шага назад")