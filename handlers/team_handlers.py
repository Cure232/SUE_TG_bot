import os 

from aiogram import F, Bot, Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext


from handlers.fsm_registration import RegistrationTeamFSM
from keyboards.reply_keyboards import (
    main_keyboard,
    teammates_keyboard,
)
from lexicon.lexicon import LEXICON
from log.logger import logger, log_registration_end
from config.config import config
from database.config import get_async_session
from database.models import User, Team
from keyboards.inline_keyboards import verify_keyboard


router = Router()

IMG_DIR = "images"

@router.message(StateFilter(RegistrationTeamFSM.fill_team_name))
async def process_team_name_registration(message: Message, state: FSMContext, bot: Bot):
    logger.info(
        f"Пользователь @{message.from_user.username} ({message.from_user.id}) вводит название команды.")

    async with get_async_session() as session:
        team_db = Team(name=message.text)
        session.add(team_db)
        await session.flush()

        await state.update_data(team_id=team_db.id)
        data: dict = await state.get_data()
        logger.info(f"Сохраняем данные в БД: {data}")
        user_db = User(**data)
        session.add(user_db)

    await message.answer(
        "\nКоманда создана!"
    )
    msg: str = f'{data["tg_link"]} {data["group_num"]} {data["game"]}'
    await bot.send_photo(chat_id=config.tg_bot.chat_id,
                         message_thread_id=config.tg_bot.chat_thread_id,
                         caption=msg,
                         photo=FSInputFile(data["st_card_photo"]),
                         reply_markup=teammates_keyboard)
    await log_registration_end(bot, message.from_user.username, message.from_user.id, data)

    await state.set_state(RegistrationTeamFSM.add_teammate)
    await message.answer(
        "Теперь можете добавить сокомандников",
        reply_markup=teammates_keyboard
    )

@router.message(F.text == LEXICON["add_teammate_button"], StateFilter(RegistrationTeamFSM.add_teammate))
async def process_teammate_start_registration(message: Message, state: FSMContext):
    logger.info(
        f"Пользователь @{message.from_user.username} начал добавление игрока ({message.from_user.id})")
    await state.set_state(RegistrationTeamFSM.fill_name)
    await message.answer(
        "Введите ФИО игрока: ",
        reply_markup=teammates_keyboard
    )

@router.message(StateFilter(RegistrationTeamFSM.fill_name))
async def process_teammate_group_registration(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.update_data(is_captain=False)
    await state.update_data(tg_link=None)
    logger.info(
        f"ФИО тиммейта {message.text} сохранено для пользователя @{message.from_user.username} ({message.from_user.id})")
    await state.set_state(RegistrationTeamFSM.fill_group)
    await message.answer(
        "Введите группу игрока: ",
        reply_markup=teammates_keyboard
    )

@router.message(StateFilter(RegistrationTeamFSM.fill_group))
async def process_teammate_steam_registration(message: Message, state: FSMContext):
    await state.update_data(group_num=message.text)
    logger.info(
        f"Номер группы тиммейта {message.text} сохранен для пользователя @{message.from_user.username} ({message.from_user.id})")
    await state.update_data()
    await state.set_state(RegistrationTeamFSM.fill_steam_lnk)
    await message.answer(
        "Введите ссылку на STEAM игрока: ",
        reply_markup=teammates_keyboard
    )

@router.message(StateFilter(RegistrationTeamFSM.fill_steam_lnk))
async def process_teammate_photo_registartion(message: Message, state: FSMContext):
    await state.update_data(steam_link=message.text)
    logger.info(
        f"Ссылка на STEAM тиммейта {message.text} сохранена для пользователя @{message.from_user.username} ({message.from_user.id})")
    await state.update_data()
    await state.set_state(RegistrationTeamFSM.fill_photo)
    await message.answer(
        "Прикрепите фотографию со студенческим: ",
        reply_markup=teammates_keyboard
    )

@router.message(StateFilter(RegistrationTeamFSM.fill_photo))
async def process_teammate_end_regisation(message: Message, state: FSMContext, bot: Bot):

    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_path = os.path.join(IMG_DIR, f"{photo.file_id}.jpg")

    os.makedirs(IMG_DIR, exist_ok=True)

    await bot.download_file(file.file_path, file_path)
    await state.update_data(st_card_photo=file_path)

    data: dict = await state.get_data()
    logger.info(f"Сохраняем данные в БД: {data}")

    async with get_async_session() as session:
        user_db = User(**data)
        session.add(user_db)
    
    msg: str = f'Тиммейт добавлен {data["name"]} {data["group_num"]} {data["game"]}'
    await bot.send_photo(chat_id=config.tg_bot.chat_id,
                         message_thread_id=config.tg_bot.chat_thread_id,
                         caption=msg,
                         photo=FSInputFile(data["st_card_photo"]),
                         reply_markup=teammates_keyboard)
    await message.answer(
        "Тиммейт добавлен", 
        reply_markup=teammates_keyboard
    )
    logger.info(
        f"Пользователь добавил тиммейта @{message.from_user.username} ({message.from_user.id})")

    await state.set_state(RegistrationTeamFSM.add_teammate)

@router.message(F.text == LEXICON["team_done_button"], StateFilter(RegistrationTeamFSM.add_teammate))
async def process_team_registration(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Команда добавлена!",
        reply_markup=main_keyboard
    )