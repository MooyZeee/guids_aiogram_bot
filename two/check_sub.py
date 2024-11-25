from typing import Dict, Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from inline_kb import channels, my_builder


class CheckSubscribe(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        for channel in channels:
            channel_name = f'@{channel[13:]}'

            # print(channel[13:])
            user_id = event.from_user.id

            surscribes = await event.bot.get_chat_member(
                chat_id=channel_name,
                user_id=user_id
            )
            if surscribes.status == 'left':
                await event.answer('Подпишитесь на каналы', reply_markup=my_builder())
                return
        else:
            return await handler(event, data)
