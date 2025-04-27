from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON


verify_keyboard_builder = InlineKeyboardBuilder()

verify_keyboard_builder.button(text=LEXICON["yes_verify_btn"], callback_data="verify_yes")
verify_keyboard_builder.button(text=LEXICON["no_verify_btn"], callback_data="verify_no")

verify_keyboard = verify_keyboard_builder.as_markup()
