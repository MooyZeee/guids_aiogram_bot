from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


keyboard_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Админ панель', callback_data='admin_panel_data')]
])

add_new_admin_user_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📝Рассылка', callback_data='newsletter_data')]
])


back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙Назад', callback_data='back_data2')]
])
