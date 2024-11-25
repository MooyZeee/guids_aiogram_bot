from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

channels = ['https://t.me/movsar_fatima', 'https://t.me/thisprojectbot']


def my_builder():
    builder = InlineKeyboardBuilder()
    for channel in channels:
        builder.button(text='Подпишись', url=channel)
    builder.adjust(1)
    return builder.as_markup()

def get_inlineMix_btns(        *,
        btns: dict[str, str],        sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    for text, value in btns.items():
        if '://' in value:
            keyboard.add(InlineKeyboardButton(text=text, url=value))
        else:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=value))
    return keyboard.adjust(*sizes).as_markup()