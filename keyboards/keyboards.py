from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon import LEXICON

button_register = KeyboardButton(text=LEXICON["register_button"])

user_keyboard_builder = ReplyKeyboardBuilder()
user_keyboard_builder.row(button_register)

user_keyboard: ReplyKeyboardBuilder = user_keyboard_builder.as_markup(
    resize_keyboard = True
)