from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from keyboards.keyboards import user_keyboard
from lexicon.lexicon import LEXICON

router = Router()

@router.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.reply(LEXICON["/start"], reply_markup=user_keyboard)

@router.message(Command(commands="register"))
async def process_register_command(message: Message):
    await message.reply(LEXICON["/register"], reply_markup=user_keyboard)

@router.message(Command(commands="help"))
async def process_register_command(message: Message):
    await message.reply(LEXICON["/help"], reply_markup=user_keyboard)

