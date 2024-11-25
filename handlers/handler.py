import asyncio
import logging

from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from auxiliary_functions.helper_func import *
from keyboard.keyboard import *

class Reg(StatesGroup):
    id = State()
    remove_admin = State()
    download_picture = State()
    add_new_group_name = State()
    add_new_group_username = State()
    delete_group = State()
    get_player_id = State()
    text = State()


logging.basicConfig(level=logging.INFO)
router = Router()


# Функция для вызова кнопки перенаправления в админ панель
async def send_admin_panel(message: Message):
    await message.answer('Вам доступна админская часть!', reply_markup=keyboard_main)


# Функция отправки видео/гайда
async def send_guid(message: Message):
    # # Вызов корутины отправки сообщения в переменной, дабы удаления сообщений после успешной обработки
    # a = await message.answer('Видео отправляется...')
    # input_file = 'info_video.mov'
    # output_file = 'compressed_video.mov'
    #
    # # Сжимаем видео
    # clip = VideoFileClip(input_file)
    # clip = clip.resized(height=1080)  # Измените разрешение
    # clip.write_videofile(output_file, codec='libx264', bitrate='500k')
    #
    #
    # # Отправляем сжатое видео
    # try:
    #     async with aiofiles.open(output_file, 'rb') as file:
    #         video = BufferedInputFile(await file.read(), filename=output_file)
    #         await message.bot.send_video(
    #             chat_id=message.chat.id,
    #             video=video,
    #             caption='Ловите гайд как сделать прекрасные Сторис с большим охватом;'
    #         )

    # Удаляем сообщение которые вызывается с помощью корутины
    # await a.delete()

    # except FileNotFoundError:
    #     print("Файл не найден.")
    #     await message.answer("Файл видео не найден. Пожалуйста, проверьте путь к файлу.")
    # except Exception as e:
    #     print(f"Ошибка при отправке видео: {e}")
    #     await message.answer("Произошла ошибка при отправке видео. Попробуйте позже.")

    await message.answer(
        'Держи бесплатный урок, как снимать сторисы, чтобы охваты постоянно росли! \n\n https://youtu.be/cD60phCue7o?si=kp4eVrOVYfrk-2Qc', disable_web_page_preview=False)


# Функция создания клавиатуры с группами из JSON-формата файла
async def handle_subscription_check(message: Message, groups):
    not_subscribed_channels = []

    list_admins = checked_admin_list()
    if message.from_user.id in list_admins:
        return []  # Если это администратор, не проверяем подписки

    for group in groups:
        member = await message.bot.get_chat_member(chat_id=f'@{group["username"]}', user_id=message.from_user.id)
        print(f"Checking {group['username']}: {member.status}: {message.from_user.id}")  # Отладочная информация
        if member.status not in ['member', 'creator', 'administrator']:
            not_subscribed_channels.append(group)

    return not_subscribed_channels


# Функция для ассинхронного ожидания проверки подписок
async def periodic_subscription_check(message: Message, groups):
    await asyncio.sleep(1)  # Задержка 4 часа (14400 секунд)

    not_subscribed_channels = await handle_subscription_check(message, groups)

    if not_subscribed_channels:
        # Если пользователь не подписан на каналы
        keyboard = [
            [InlineKeyboardButton(text=channel["name"], url=f'https://t.me/{channel["username"]}') for channel in not_subscribed_channels],
            [InlineKeyboardButton(text='Проверить подписку', callback_data='check_subscribes')]
        ]
        keyboard_subscribe = InlineKeyboardMarkup(inline_keyboard=keyboard)

        await message.answer(
            'Подпишись на мой телеграмм канал. Там я делюсь новыми алгоритмами инстаграм, фишками, делаю бесплатные разборы аккаунтов🔥',
                             reply_markup=keyboard_subscribe)
        print("Message sent asking for subscription with channels.")
    else:
        print("User is subscribed to all channels. No message sent.")



@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    groups = load_from_json()
    admin = checked_admin_list()
    check_user = get_anonim(message.from_user.id)

    logging.info(f"check_user: {check_user}, user_id: {message.from_user.id}, admin_list: {admin}")

    if not check_user:
        write_user_id(message.from_user.id)
        await send_guid(message)
    if check_user:
        await send_guid(message)
    if message.from_user.id in admin:
        await send_admin_panel(message)

    # Запускаем периодическую проверку подписок в отдельной задаче
    asyncio.create_task(periodic_subscription_check(message, groups))


@router.callback_query(F.data == 'check_subscribes')
async def check_subscribes(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    not_subscribed_channels = []
    groups = load_from_json()

    try:
        for i in groups:
            member = await callback_query.bot.get_chat_member(chat_id=f'@{i["username"]}', user_id=user_id)
            if member.status not in ['member', 'creator', 'administrator']:
                not_subscribed_channels.append(i["username"])

        if not_subscribed_channels:
            # Если есть неподписанные каналы, отправляем сообщение
            keyboard_subscribe = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=channel, url=f'https://t.me/{channel}') for channel in not_subscribed_channels]
            ])

            await callback_query.message.answer(
                'Подпишись на мой телеграмм канал. Там я делюсь новыми алгоритмами инстаграм, фишками, делаю бесплатные разборы аккаунтов🔥',
                reply_markup=keyboard_subscribe)
            await callback_query.answer('Warning!')

        else:
            await callback_query.message.answer('Благодарим вас за поддержку! Вы очень помогаете нам своими подписками!')
            await callback_query.answer('Благодарим вам. До свидания!')

    except Exception as e:
        print(f"Error checking subscriptions: {e}")
        await callback_query.answer("Произошла ошибка при проверке подписок.")


@router.callback_query(F.data == 'back_data2')
async def back_data_func(callback: CallbackQuery):
    await callback.message.edit_text('Перенаправляем вас в админ панель: ', reply_markup=add_new_admin_user_keyboard)


# Коллбек для установки состояния для рассылки
@router.callback_query(F.data == 'newsletter_data')
async def newsletter_func(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Отправьте (Фото/Текст/Текст и Фото вместе)', reply_markup=back_keyboard)
    await state.set_state(Reg.text)


# Функция для рассылки сообщений
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@router.message(F.content_type.in_({ContentType.TEXT, ContentType.PHOTO, ContentType.VIDEO}), Reg.text)
async def process_mixed_content(message: Message, state: FSMContext):
    groups = load_from_json()
    all_user_ids = get_all_user()
    text = message.caption if message.caption else message.text
    photo = message.photo[-1].file_id if message.photo else None
    video = message.video.file_id if message.video else None

    for user_id in all_user_ids:
        try:
            user_id_int = int(user_id)

            # Проверка подписки для текущего пользователя
            not_subscribed_channels = await handle_subscription_check(message, groups)

            if not_subscribed_channels:
                # Если пользователь не подписан на каналы, создаем клавиатуру
                keyboard_subscribe = [
                    [InlineKeyboardButton(text=channel["name"], url=f'https://t.me/{channel["username"]}') for channel in not_subscribed_channels],
                    [InlineKeyboardButton(text='Проверить подписку', callback_data='check_subscribes')]
                ]
                keyboard_markup = InlineKeyboardMarkup(inline_keyboard=keyboard_subscribe)

                await message.bot.send_message(chat_id=user_id_int,
                                               text='Подпишись на мой телеграмм канал. Там я делюсь новыми алгоритмами инстаграм, фишками, делаю бесплатные разборы аккаунтов🔥',
                                               reply_markup=keyboard_markup)
                print(f"Сообщение с просьбой о подписке отправлено пользователю {user_id_int}")
            else:
                # Отправка сообщения пользователю только если он подписан
                if text and photo:
                    await message.bot.send_photo(chat_id=user_id_int, photo=photo, caption=text)
                elif text and video:
                    await message.bot.send_video(chat_id=user_id_int, video=video, caption=text)
                elif text:
                    await message.bot.send_message(chat_id=user_id_int, text=text)
                elif photo:
                    await message.bot.send_photo(chat_id=user_id_int, photo=photo)
                elif video:
                    await message.bot.send_video(chat_id=user_id_int, video=video)

                print(f"Сообщение успешно отправлено пользователю {user_id_int}")

        except Exception as e:
            await message.bot.send_message(message.chat.id, f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

    await message.answer("Рассылка завершена.")
    await state.clear()

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Рассылка 📝", callback_data='newsletter_data')]
    ])

    await message.answer("Выберите действие:", reply_markup=keyboard)



@router.message(Command('admin_panel'))
@router.callback_query(F.data == 'admin_panel_data')
async def send_guids_callback(message_or_callback: Message | CallbackQuery):
    if isinstance(message_or_callback, CallbackQuery):
        # Если это CallbackQuery, то получаем сообщение из колбека
        await message_or_callback.message.edit_text('Используйте все наши функции', reply_markup=add_new_admin_user_keyboard)
    else:
        # Если это Message (команда), то просто вызываем send_guid
        await message_or_callback.answer('Используйте все наши функции', reply_markup=add_new_admin_user_keyboard)
