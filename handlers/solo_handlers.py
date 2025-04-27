import os
import re

from aiogram import F, Bot, Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from handlers.fsm_registration import RegistrationSoloFSM
from keyboards.reply_keyboards import (
    main_keyboard,
    main_game_keyboard,
    main_team_or_solo_keyboard,
    teammates_keyboard,
    main_cancel_registration_keyboard
)
from keyboards.inline_keyboards import verify_keyboard
from lexicon.lexicon import LEXICON
from database.config import get_async_session
from database.models import User
from config.config import config
from log.logger import log_registration_end, logger


router = Router()

IMG_DIR = "images"


@router.message(F.text == LEXICON["register_button"], StateFilter(default_state))
@router.message(Command(commands="register"))
async def process_register_command(message: Message, state: FSMContext):
    logger.info(
        f"Регистрация начата пользователем @{message.from_user.username} ({message.from_user.id})")
    await state.update_data(tg_link=message.from_user.username)
    await state.update_data(is_captain=True)
    await state.set_state(RegistrationSoloFSM.fill_name)
    await message.answer(
        "Начата регистрация на турнир. \n"
        "\nНапишите ваше ФИО.",
        reply_markup=main_cancel_registration_keyboard
    )


@router.message(StateFilter(RegistrationSoloFSM.fill_name), lambda message: not re.fullmatch(r'[А-Яа-яёЁ ]{,100}', message.text))
async def process_name_registration(message: Message):
    logger.warning(
        f"Неверный формат имени от пользователя @{message.from_user.username} ({message.from_user.id})")
    await message.reply(
        "Данные введены в неверном формате",
        reply_markup=main_cancel_registration_keyboard
    )


@router.message(StateFilter(RegistrationSoloFSM.fill_name))
async def process_name_registration(message: Message, state: FSMContext):
    logger.info(
        f"Имя пользователя {message.text} сохранено для @{message.from_user.username} ({message.from_user.id})")
    await state.update_data(name=message.text)
    await state.set_state(RegistrationSoloFSM.fill_group)
    await message.answer(
        "Данные сохранены. \n"
        "\nВведите номер группы.  ",
        reply_markup=main_cancel_registration_keyboard
    )


@router.message(StateFilter(RegistrationSoloFSM.fill_group), lambda message: not re.fullmatch(r'[0-9A-Z- ]{,20}', message.text))
async def process_group_registration(message: Message):
    logger.warning(
        f"Неверный формат номера группы от пользователя @{message.from_user.username} ({message.from_user.id})")
    await message.reply(
        "Данные введены в неверном формате",
        reply_markup=main_cancel_registration_keyboard
    )


@router.message(StateFilter(RegistrationSoloFSM.fill_group))
async def process_group_registration(message: Message, state: FSMContext):
    logger.info(
        f"Номер группы {message.text} сохранен для пользователя @{message.from_user.username} ({message.from_user.id})")
    await state.update_data(group_num=message.text)
    await state.set_state(RegistrationSoloFSM.fill_steam_lnk)
    await message.answer(
        "Данные сохранены. \n"
        "\nВведите ссылку на STEAM. ",
        reply_markup=main_cancel_registration_keyboard
    )


@router.message(StateFilter(RegistrationSoloFSM.fill_steam_lnk), lambda message: not re.fullmatch(r'https://steamcommunity.com/\S+', message.text))
async def process_link_registration(message: Message):
    logger.warning(
        f"Неверный формат ссылки на STEAM от пользователя @{message.from_user.username} ({message.from_user.id})")
    await message.reply(
        "Данные введены в неверном формате",
        reply_markup=main_cancel_registration_keyboard
    )


@router.message(StateFilter(RegistrationSoloFSM.fill_steam_lnk))
async def process_link_registration(message: Message, state: FSMContext):
    logger.info(
        f"Ссылка на STEAM {message.text} сохранена для пользователя @{message.from_user.username} ({message.from_user.id})")
    await state.update_data(steam_link=message.text)
    await state.set_state(RegistrationSoloFSM.fill_photo)
    await message.answer(
        "Данные сохранены. \n"
        "\nПрикрепите фотографию студенческого для верификации. ",
        reply_markup=main_cancel_registration_keyboard
    )


@router.message(StateFilter(RegistrationSoloFSM.fill_photo), F.photo)
async def process_photo_registration(message: Message, state: FSMContext, bot: Bot):
    logger.info(
        f"Пользователь @{message.from_user.username} ({message.from_user.id}) загрузил фото студенческого.")
    photo = message.photo[-1]

    file = await bot.get_file(photo.file_id)
    file_path = os.path.join(IMG_DIR, f"{photo.file_id}.jpg")

    os.makedirs(IMG_DIR, exist_ok=True)

    await bot.download_file(file.file_path, file_path)

    await state.update_data(st_card_photo=file_path)
    await state.set_state(RegistrationSoloFSM.fill_game)
    await message.answer(
        "Данные сохранены. \n"
        "\nВыберите дисциплину для турнира",
        reply_markup=main_game_keyboard
    )


@router.message(StateFilter(RegistrationSoloFSM.fill_photo))
async def process_photo_registration(message: Message):
    logger.warning(
        f"Пользователь @{message.from_user.username} ({message.from_user.id}) отправил неверный формат фото.")
    await message.reply(
        "Данные введены в неверном формате",
        reply_markup=main_cancel_registration_keyboard
    )


@router.message(F.text.in_({LEXICON["dota_game_button"], LEXICON["cs_game_button"]}),
                StateFilter(RegistrationSoloFSM.fill_game))
async def process_game_registration(message: Message, state: FSMContext):
    logger.info(
        f"Пользователь @{message.from_user.username} ({message.from_user.id}) выбрал дисциплину {message.text}")
    await state.update_data(game=message.text)
    await state.set_state(RegistrationSoloFSM.team_or_solo)
    await message.answer(
        f"Выбрана дисциплина {message.text}\n"
        "\nВы хотите зарегистрировть себя или команду?",
        reply_markup=main_team_or_solo_keyboard
    )


@router.message(F.text == LEXICON["team_button"], StateFilter(RegistrationSoloFSM.team_or_solo))
async def process_team_registration(message: Message, state: FSMContext):
    logger.info(
        f"Пользователь @{message.from_user.username} ({message.from_user.id}) выбрал регистрацию команды.")
    await state.update_data(team_id=None)
    await state.set_state(RegistrationSoloFSM.fill_team_name)
    await message.answer(
        "\nВведите название вашей команды",
        reply_markup=teammates_keyboard
    )


@router.message(F.text == LEXICON["solo_button"], StateFilter(RegistrationSoloFSM.team_or_solo))
async def process_solo_registration(message: Message, state: FSMContext, bot: Bot):
    logger.info(
        f"Пользователь @{message.from_user.username} ({message.from_user.id}) выбрал регистрацию как соло.")
    await state.update_data(team_id=None)

    data: dict = await state.get_data()
    logger.info(f"Сохраняем данные в БД: {data}")

    async with get_async_session() as session:
        user_db = User(**data)
        session.add(user_db)

    await state.clear()
    await message.answer(
        "\nРегистрация завершена!",
        reply_markup=main_keyboard
    )
    msg: str = f'{data["tg_link"]} {data["group_num"]} {data["game"]}'
    await bot.send_photo(chat_id=config.tg_bot.chat_id,
                         message_thread_id=config.tg_bot.chat_thread_id,
                         caption=msg,
                         photo=FSInputFile(data["st_card_photo"]),
                         reply_markup=verify_keyboard)
    await log_registration_end(bot, message.from_user.username, message.from_user.id, data)
    logger.info(
        f"Логирование завершено для пользователя @{message.from_user.username} ({message.from_user.id})")


@router.message(StateFilter(RegistrationSoloFSM.fill_team_name))
async def process_team_name_registration(message: Message, state: FSMContext):
    logger.info(
        f"Пользователь @{message.from_user.username} ({message.from_user.id}) вводит название команды.")
    await state.update_data(team_name=message.text)
    await state.set_state(RegistrationSoloFSM.add_teammate)
    await state.update_data(teammates=[])
    await message.answer(
        "Теперь можете добавить сокомандников",
        reply_markup=teammates_keyboard
    )
