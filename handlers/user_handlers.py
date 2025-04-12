from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import PhotoSize

from handlers.fsm_registration import (
    TeamRegistration,
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

@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        "Вы вышли завершили регистрацию."
        )
    await state.clear()

@router.message(F.text == LEXICON["register_button"])
@router.message(Command(commands="register"))
async def process_register_command(message: Message):
    await message.answer(
        "Начата регистрация команды на турнир. \n" 
        "\nВ какой дисциплине вы хотите принять участие?",
        reply_markup=main_game_keyboard
        )

@router.message(F.text == LEXICON["cs_game_button"])
async def process_cs_registration(message: Message, state: FSMContext):
    await message.answer(
        "Выбрана дисциплина Counter - Strike 2 \n" 
        "\nВведите название команды.  "
        )
    await state.set_state(TeamRegistration.fill_team_name)

@router.message(F.text == LEXICON["dota_game_button"])
async def process_dota_registration(message: Message, state: FSMContext):
    await message.answer(
        "Выбрана дисциплина Counter - Strike 2 \n" 
        "\nВведите название команды.  "
        )
    await state.set_state(TeamRegistration.fill_team_name)

@router.message(StateFilter(TeamRegistration.fill_team_name))
async def process_team_name_registration(message: Message, state: FSMContext):
    await state.update_data(fill_team_name=message.text)
    await message.answer(
        "Данные сохранены. \n" 
        "\nВведите ФИО.  "
        )
    COUNTER = 0
    await state.set_state(TeamRegistration.fill_name)

@router.message(StateFilter(TeamRegistration.fill_name), F.text.isalpha())
async def process_name_registration(message: Message, state: FSMContext):
    await state.update_data(fill_name=message.text)
    await message.answer(
        "Данные сохранены. \n" 
        "\nВведите номер группы.  "
        )
    await state.set_state(TeamRegistration.fill_group)    

@router.message(StateFilter(TeamRegistration.fill_group))
async def process_group_registration(message: Message, state: FSMContext):
    await state.update_data(fill_group=message.text)
    await message.answer(
        "Данные сохранены. \n" 
        "\nВведите ссылку на STEAM. "
        )
    await state.set_state(TeamRegistration.fill_link)  

@router.message(StateFilter(TeamRegistration.fill_link))
async def process_link_registration(message: Message, state: FSMContext):
    await state.update_data(fill_link=message.text)
    await message.answer(
        "Данные сохранены. \n" 
        "\nПрикрепите фотографию студенческого для верификации. "
        )
    await state.set_state(TeamRegistration.fill_photo)

@router.message(StateFilter(TeamRegistration.fill_photo), F.photo)
async def process_photo_registration(message: Message, state: FSMContext):
    first_photo = message.photo[0]
    await state.update_data(fill_photo=first_photo.file_id)
    data = await state.get_data()
    team_counter = data.get("team_counter", 0)
    team_counter += 1
    await state.update_data(team_counter=team_counter)
    if team_counter < 5:
        await message.answer(
            "Данные сохранены. \n" 
            "\nВведите фио следующего игрока "
            )
        await state.set_state(TeamRegistration.fill_name) 
    else:
        await message.answer(
        "Регистрация завершена!",
        )
        await state.clear() 


@router.message(F.text == LEXICON["back_button"])
async def prcess_back_registration(message: Message):
    await message.answer("Тут будет реализация шага назад")