import os
import logging
import re

from aiogram import F, Bot, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from handlers.fsm_registration import (
    RegistrationFSM,
    RegistrationTeamFSM
)
from keyboards.keyboards import (
    main_keyboard,
    main_game_keyboard,
    main_team_or_solo_keyboard,
    teammates_keyboard,
    main_cancel_registration_keyboard,
    main_cancel_registration_choice_keyboard
)
from lexicon.lexicon import LEXICON
from lexicon.commands import COMMANDS
from database.config import get_async_session
from database.schemas import UserCreate
from database.models import User, Team

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [%(funcName)s] %(message)s',
    handlers={logging.StreamHandler()}
)

router = Router()

IMG_DIR = "images"

@router.message(Command(commands='start'))
async def process_start_command(message: Message, state:FSMContext):
    await state.clear()
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

@router.message(F.text == COMMANDS["/cancel"])
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        "Вы точно хотите прекратить процесс регистрации?",
        reply_markup=main_cancel_registration_choice_keyboard
    )

@router.message(F.text == LEXICON["yes_stop_button"], ~StateFilter(default_state))
async def process_stop_registration(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "\n Регистрация прекращена",
        reply_markup=main_keyboard
    )

@router.message(F.text == LEXICON["no_stop_button"], ~StateFilter(default_state))
async def process_stop_registration(message: Message, state: FSMContext):
    await message.answer(
        "\n Продолжайте регистрацию",
        reply_markup=main_cancel_registration_keyboard
    )

@router.message(F.text == LEXICON["register_button"], StateFilter(default_state))
@router.message(Command(commands="register"))
async def process_register_command(message: Message, state: FSMContext):
    await state.update_data(tg_link=message.from_user.username)
    await state.update_data(is_captain=True)
    await state.set_state(RegistrationFSM.fill_name)
    await message.answer(
        "Начата регистрация на турнир. \n"
        "\nНапишите ваше ФИО.",
        reply_markup=main_cancel_registration_keyboard
    )

@router.message(StateFilter(RegistrationFSM.fill_name), lambda message: not re.fullmatch(r'[А-Яа-яёЁ ]{,100}' , message.text))
async def process_name_registration(message: Message):
    await message.reply(
        "Данные введены в неверном формате",
        reply_markup=main_cancel_registration_keyboard
    )

@router.message(StateFilter(RegistrationFSM.fill_name))
async def process_name_registration(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RegistrationFSM.fill_group)
    await message.answer(
        "Данные сохранены. \n"
        "\nВведите номер группы.  ",
        reply_markup=main_cancel_registration_keyboard
    )

@router.message(StateFilter(RegistrationFSM.fill_group), lambda message: not re.fullmatch(r'[0-9A-Z- ]{,20}' , message.text))
async def process_group_registration(message: Message):
    await message.reply(
        "Данные введены в неверном формате",
        reply_markup=main_cancel_registration_keyboard
    )

@router.message(StateFilter(RegistrationFSM.fill_group))
async def process_group_registration(message: Message, state: FSMContext):
    await state.update_data(group_num=message.text)
    await state.set_state(RegistrationFSM.fill_steam_lnk)
    await message.answer(
        "Данные сохранены. \n"
        "\nВведите ссылку на STEAM. ",
        reply_markup=main_cancel_registration_keyboard
    )

@router.message(StateFilter(RegistrationFSM.fill_steam_lnk), lambda message: not re.fullmatch(r'https://steamcommunity.com/\S+' , message.text))
async def process_link_registration(message: Message):
    await message.reply(
        "Данные введены в неверном формате",
        reply_markup=main_cancel_registration_keyboard
    )

@router.message(StateFilter(RegistrationFSM.fill_steam_lnk))
async def process_link_registration(message: Message, state: FSMContext):
    await state.update_data(steam_link=message.text)
    await state.set_state(RegistrationFSM.fill_photo)
    await message.answer(
        "Данные сохранены. \n"
        "\nПрикрепите фотографию студенческого для верификации. ",
        reply_markup=main_cancel_registration_keyboard
    )


@router.message(StateFilter(RegistrationFSM.fill_photo), F.photo)
async def process_photo_registration(message: Message, state: FSMContext, bot: Bot):
    photo = message.photo[-1]

    file = await bot.get_file(photo.file_id)
    file_path = os.path.join(IMG_DIR, f"{photo.file_id}.jpg")

    os.makedirs(IMG_DIR, exist_ok=True)

    await bot.download_file(file.file_path, file_path)

    await state.update_data(st_card_photo=file_path)
    await state.set_state(RegistrationFSM.fill_game)
    await message.answer(
        "Данные сохранены. \n"
        "\nВыберите дисциплину для турнира",
        reply_markup=main_game_keyboard
    )

@router.message(StateFilter(RegistrationFSM.fill_photo))
async def process_photo_registration(message: Message):
    await message.reply(
        "Данные введены в неверном формате",
        reply_markup=main_cancel_registration_keyboard
    )

@router.message(F.text.in_({LEXICON["dota_game_button"], LEXICON["cs_game_button"]}),
                StateFilter(RegistrationFSM.fill_game))
async def process_game_registration(message: Message, state: FSMContext):
    await state.update_data(game=message.text)
    await state.set_state(RegistrationFSM.team_or_solo)
    await message.answer(
        f"Выбрана дисциплина {message.text}\n"
        "\nВы хотите зарегистрировть себя или команду?",
        reply_markup=main_team_or_solo_keyboard
    )

@router.message(F.text == LEXICON["team_button"], StateFilter(RegistrationFSM.team_or_solo))
async def process_team_registration(message: Message, state: FSMContext):
    await state.update_data(team_id=None)
    await state.set_state(RegistrationFSM.fill_team_name)
    await message.answer(
        "\nВведите название вашей команды",
        reply_markup=teammates_keyboard
    )

@router.message(F.text == LEXICON["solo_button"], StateFilter(RegistrationFSM.team_or_solo))
async def process_solo_registration(message: Message, state: FSMContext):
    await state.update_data(team_id=None)
    
    async with get_async_session() as session:
        data: dict = await state.get_data()
        print(data)
        user_db = User(**data)
        session.add(user_db)

    await state.clear()
    await message.answer(
        "\nРегистрация завершена!",
        reply_markup=main_keyboard
    )

@router.message(StateFilter(RegistrationFSM.fill_team_name))
async def process_team_name_registration(message: Message, state: FSMContext):
    await state.update_data(team_name=message.text)
    await state.set_state(RegistrationFSM.add_teammate)
    await state.update_data(teammates=[])
    data = await state.get_data()
    name = data.get("name")
    group = data.get("group")
    tg_link = data.get("tg_link")
    steam_link = data.get("steam_link")
    st_card_photo = data.get("st_card_photo")
    game = data.get("game")
    async with get_async_session() as session:
        new_team = Team(name=data.get("team_name"))
        session.add(new_team)
        await session.commit() 
        await session.refresh(new_team) 
        new_user = User(
            name=name,
            group_num=group,
            tg_link=tg_link,
            steam_link=steam_link,
            st_card_photo=st_card_photo,
            is_captain=True,
            game=game,
            team_id=new_team.id
        )
        session.add(new_user)
        await session.commit()
    await state.update_data(team_id=new_team.id)
    await message.answer(
        "Теперь можете добавить сокомандников",
        reply_markup=teammates_keyboard
    )

@router.message(F.text == LEXICON["add_teammate_button"])
async def process_teammate_start_registration(message: Message, state: FSMContext):
    await state.set_state(RegistrationTeamFSM.fill_name)
    await message.answer(
        "Введите ФИО игрока: ",
        reply_markup=teammates_keyboard
    )



@router.message(StateFilter(RegistrationFSM.fill_teammate_data))
async def handle_teammate_data(message: Message, state: FSMContext, bot: Bot):
    text = message.caption
    if not handle_teammate_data_check(text) or not message.photo:
        await message.answer("Пожалуйста, в одном сообщении отправьте текст с данными и фото студенческого.")
        return

    lines = text.strip().split('\n')
    photo = message.photo[-1]
    name = lines[0].strip()
    group = lines[1].strip()
    steam_link = lines[2].strip()
    tg_link = lines[3].strip()
    file = await bot.get_file(photo.file_id)
    file_path = os.path.join(IMG_DIR, f"{photo.file_id}.jpg")
    await bot.download_file(file.file_path, file_path)

    new_user = User(
        name=name,
        group_num=group,
        tg_link=tg_link,
        steam_link=steam_link,
        st_card_photo=file_path,
        is_captain=False,
        game=state.get_data()["game"],
        team_id=state.get_data()["team_id"]
    )
    async with get_async_session() as session:
        session.add(new_user)
        await session.commit()
    await message.answer("Сокомандник добавлен. Переходим к следующему этапу.")
    await state.set_state(RegistrationFSM.fill_teammate_data)

@router.message(StateFilter(RegistrationTeamFSM.fill_steam_lnk))
async def process_teammate_photo_registartion(message: Message, state: FSMContext):
    await state.update_data()
    await state.set_state(RegistrationTeamFSM.fill_photo)
    await message.answer(
        "Прикрепите фотографию со студенческим: ",
        reply_markup=teammates_keyboard
    )

@router.message(StateFilter(RegistrationTeamFSM.fill_photo))
async def process_teammate_end_regisation(message: Message, state: FSMContext):
    await state.update_data()
    await message.amswer(
        "Тиммейт добавлен", 
        reply_markup=teammates_keyboard
    )
    await state.clear()

@router.message(F.text == LEXICON["team_done_button"])
async def process_team_registration(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Команда добавлена!",
        reply_markup=main_keyboard
    )

@router.message(F.text == LEXICON["back_button"])
async def process_back_registration(message: Message):
    pass

import re


def handle_teammate_data_check(message: str) -> bool:
    lines = message.strip().split('\n')
    name = lines[0].strip()
    group = lines[1].strip()
    steam_link = lines[2].strip()
    tg_link = lines[3].strip()
   
    if not all([name, group, steam_link, tg_link]):
        return False
    if not re.fullmatch(r'[А-Яа-яёЁ ]{,100}' ,name):
        return False
    if not re.fullmatch(r'[0-9A-Z- ]{,20}' , group):
        return False 
    if not re.fullmatch(r'https://steamcommunity.com/\S+', steam_link):
        return False 
    if not re.fullmatch(r'[0-9A-Za-z_]+', tg_link):
        return False 
    
    return True
