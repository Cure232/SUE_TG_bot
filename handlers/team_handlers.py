import os 

from aiogram import F, Bot, Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext


from handlers.fsm_registration import (
    RegistrationSoloFSM,
    RegistrationTeamFSM
)
from keyboards.reply_keyboards import (
    main_keyboard,
    teammates_keyboard,
)
from lexicon.lexicon import LEXICON
from log.logger import logger


router = Router()

IMG_DIR = "images"

@router.message(F.text == LEXICON["team_button"], StateFilter(RegistrationSoloFSM.team_or_solo))
async def process_team_registration(message: Message, state: FSMContext):
    logger.info(
        f"Пользователь @{message.from_user.username} начал создание команды ({message.from_user.id})")
    await state.update_data(team_id=None)
    await state.set_state(RegistrationSoloFSM.fill_team_name)
    await message.answer(
        "\nВведите название вашей команды",
        reply_markup=teammates_keyboard
    )

@router.message(StateFilter(RegistrationSoloFSM.fill_team_name))
async def process_team_name_registration(message: Message, state: FSMContext):
    logger.info(
        f"Пользователь @{message.from_user.username} назвал команду ({message.from_user.id})")
    await state.update_data(team_name=message.text)
    await state.clear()
    await message.answer(
        "Теперь можете добавить сокомандников",
        reply_markup=teammates_keyboard
    )

@router.message(F.text == LEXICON["add_teammate_button"])
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
    await state.update_data(name=message.txt)
    logger.info(
        f"ФИО тиммейта {message.text} сохранено для пользователя @{message.from_user.username} ({message.from_user.id})")
    await state.set_state(RegistrationTeamFSM.fill_group)
    await message.answer(
        "Введите группу игрока: ",
        reply_markup=teammates_keyboard
    )

@router.message(StateFilter(RegistrationTeamFSM.fill_group))
async def process_teammate_steam_registration(message: Message, state: FSMContext):
    await state.update_data(group_num=message.txt)
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
    await state.update_data(steam_link=message.txt)
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
    await state.update_data(name=message.txt)
    logger.info(
        f"Пользователь @{message.from_user.username} ({message.from_user.id}) загрузил фото студенческого тиммейта.")
    await state.update_data()
    await message.amswer(
        "Тиммейт добавлен", 
        reply_markup=teammates_keyboard
    )
    logger.info(
        f"Пользователь добавил тиммейта @{message.from_user.username} ({message.from_user.id})")

    await state.clear()

@router.message(F.text == LEXICON["team_done_button"])
async def process_team_registration(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Команда добавлена!",
        reply_markup=main_keyboard
    )