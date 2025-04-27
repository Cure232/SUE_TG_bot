from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from keyboards.reply_keyboards import (
    main_keyboard,
    main_cancel_registration_keyboard,
    main_cancel_registration_choice_keyboard
)
from lexicon.lexicon import LEXICON
from lexicon.commands import COMMANDS
from log.logger import log_registration_start, logger


router = Router()


@router.message(Command(commands='start'))
async def process_start_command(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    await message.reply(
        LEXICON["/start"],
        reply_markup=main_keyboard
    )
    logger.info(
        f"Пользователь @{message.from_user.username} запустил бота (/start)")
    await log_registration_start(bot, message.from_user.username, message.from_user.id)


@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.reply(
        LEXICON["/help"],
        reply_markup=main_keyboard
    )
    logger.info(
        f"Пользователь @{message.from_user.username} запросил помощь (/help)")


@router.message(F.text == COMMANDS["/cancel"])
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        "Вы точно хотите прекратить процесс регистрации?",
        reply_markup=main_cancel_registration_choice_keyboard
    )
    logger.info(
        f"Пользователь @{message.from_user.username} запросил отмену регистрации (/cancel)")


@router.message(F.text == LEXICON["yes_stop_button"], ~StateFilter(default_state))
async def process_stop_registration(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "\n Регистрация прекращена",
        reply_markup=main_keyboard
    )
    logger.info(
        f"Пользователь @{message.from_user.username} подтвердил прекращение регистрации")


@router.message(F.text == LEXICON["no_stop_button"], ~StateFilter(default_state))
async def process_stop_registration(message: Message, state: FSMContext):
    await message.answer(
        "\n Продолжайте регистрацию",
        reply_markup=main_cancel_registration_keyboard
    )
    logger.info(
        f"Пользователь @{message.from_user.username} отказался прекращать регистрацию")


@router.message(F.text == LEXICON["back_button"])
async def process_back_registration(message: Message):
    logger.info(
        f"Пользователь @{message.from_user.username} нажал кнопку 'Назад'")
    pass
