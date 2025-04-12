from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command

from keyboards.keyboards import (
    user_keyboard,
    user_choose_keyboard
    )
from lexicon.lexicon import LEXICON

router = Router()

@router.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.reply(LEXICON["/start"], reply_markup=user_keyboard)

@router.message(F.text == LEXICON["register_button"])
@router.message(Command(commands="register"))
async def process_register_command(message: Message):
    await message.reply(LEXICON["/register"], reply_markup=user_choose_keyboard)

@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.reply(LEXICON["/help"], reply_markup=user_keyboard)

@router.message(F.text == LEXICON["cs_choose_button"])
async def prcess_cs_registration(message: Message):
    await message.answer("Тут будет реализация регистрации КС")

@router.message(F.text == LEXICON["dota_choose_button"])
async def prcess_dota_registration(message: Message):
    await message.answer("Тут будет реализация регистрации Дота")

@router.message(F.text == LEXICON["back_button"])
async def prcess_back_registration(message: Message):
    await message.answer("Тут будет реализация шага назад")