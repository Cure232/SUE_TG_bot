from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon import LEXICON

button_register = KeyboardButton(text=LEXICON["register_button"])
button_cs_choose = KeyboardButton(text=LEXICON["cs_choose_button"])
button_dota_choose = KeyboardButton(text=LEXICON["dota_choose_button"])
button_back = KeyboardButton(text=LEXICON["back_button"])

user_keyboard_builder = ReplyKeyboardBuilder()
user_keyboard_builder.row(button_register)

user_keyboard: ReplyKeyboardBuilder = user_keyboard_builder.as_markup(
    resize_keyboard = True
)

user_keyboard_choose_builder = ReplyKeyboardBuilder()
user_keyboard_choose_builder.row(button_cs_choose, button_dota_choose, button_back, width=2)

user_choose_keyboard: ReplyKeyboardBuilder = user_keyboard_choose_builder.as_markup(
    resize_keyboard = True
)