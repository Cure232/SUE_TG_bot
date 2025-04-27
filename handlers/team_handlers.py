from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext


from handlers.fsm_registration import RegistrationTeamFSM
from keyboards.reply_keyboards import (
    main_keyboard,
    teammates_keyboard,
)
from lexicon.lexicon import LEXICON
from log.logger import logger


router = Router()


@router.message(F.text == LEXICON["add_teammate_button"])
async def process_teammate_start_registration(message: Message, state: FSMContext):
    logger.info(
        f"Пользователь @{message.from_user.username} ({message.from_user.id}) начал регистрацию тиммейта.")
    await state.set_state(RegistrationTeamFSM.fill_name)
    await message.answer(
        "Введите ФИО игрока: ",
        reply_markup=teammates_keyboard
    )


@router.message(StateFilter(RegistrationTeamFSM.fill_steam_lnk))
async def process_teammate_photo_registartion(message: Message, state: FSMContext):
    logger.info(
        f"Пользователь @{message.from_user.username} ({message.from_user.id}) предоставил ссылку STEAM для тиммейта.")
    await state.update_data()
    await state.set_state(RegistrationTeamFSM.fill_photo)
    await message.answer(
        "Прикрепите фотографию со студенческим: ",
        reply_markup=teammates_keyboard
    )


@router.message(StateFilter(RegistrationTeamFSM.fill_photo))
async def process_teammate_end_regisation(message: Message, state: FSMContext):
    logger.info(
        f"Пользователь @{message.from_user.username} ({message.from_user.id}) завершил добавление тиммейта.")
    await state.update_data()
    await message.answer(
        "Тиммейт добавлен",
        reply_markup=teammates_keyboard
    )
    await state.clear()


@router.message(F.text == LEXICON["team_done_button"])
async def process_team_registration(message: Message, state: FSMContext):
    logger.info(
        f"Пользователь @{message.from_user.username} ({message.from_user.id}) завершил регистрацию команды.")
    await state.clear()
    await message.answer(
        "Команда добавлена!",
        reply_markup=main_keyboard
    )
