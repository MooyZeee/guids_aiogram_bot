import asyncio
import logging
import sqlite3

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from check_sub import CheckSubscribe

from inline_kb import channels, my_builder, get_inlineMix_btns

TOKEN = '7571560301:AAFQb0-Tj5a1XpR1Mq-q2iB6DNQG5TxVdYA'
id = '5671959661'

admin_list = ['7455294297']
bot = Bot(token=TOKEN)
dp = Dispatcher()


class Form(StatesGroup):
    id = State()


class AddChanel(StatesGroup):
    name = State()
    url = State()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('hello')


@dp.message(Command('admin'))
async def create(message: Message):
    await message.answer('Что хотите сделать', reply_markup=get_inlineMix_btns(btns={
        'Добавить Канал🗣': 'add_chanel',
        'Удалить Канал❌': 'delete_chanel',
        'Мои каналы👥': 'my_chanels'
    }, sizes=(1, 1)))


### Добавление ссылок
@dp.callback_query(F.data == 'add_chanel')
async def add_chanel(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Добавить канал')
    await state.set_state(AddChanel.url)
    await callback.message.answer('Введите ссылку на канал который хотите добавить')


@dp.message(AddChanel.url)
async def chane_name(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    data = await state.get_data()
    channels.append(data['url'])
    url = data['url']
    if url:
        await message.answer('Канал добавлен', reply_markup=my_builder())
        await state.clear()
    else:
        await message.answer('Вы не правильно ввели ссылку или допустили ошибку в ссылку введите заново')
    await state.clear()


### Добавление ссылок


# Мои каналы
@dp.callback_query(F.data == 'my_chanels')
async def my_chanels(callback: CallbackQuery):
    await callback.answer('Ващи каналы')
    await callback.message.answer('Ваши каналы', reply_markup=my_builder())


# Мои каналы

async def main():
    dp.message.middleware(CheckSubscribe())
    await dp.start_polling(bot)
    logging.basicConfig(level=logging.INFO)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Выход')
