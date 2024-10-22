import asyncio
from typing import Callable, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message


class AlbumMiddleware(BaseMiddleware):

    album_data: dict = {}

    def __init__(self, latency: Union[int, float]=4):
        self.latency = latency


    async def __call__(self,
                       handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
                       message: Message,
                       data: dict[str, Any]):

        if not message.media_group_id:
            #если сообщение не медиа группа, то просто выполнить хэндлер и выйти
            await handler(message, data)
            return

        try:
            #если сообщ - медиагруппа, то добавить в сущ. словарь под ключом сообщение, которое было отправлено
            self.album_data[message.media_group_id].append(message)

        except KeyError:
            #Если такого ключа не сущ., то создаем его и туда в списке склдываем сообщение
            self.album_data[message.media_group_id] = [message]

            await asyncio.sleep(self.latency)

            data['_is_last'] = True
            data["album"] = self.album_data[message.media_group_id]

            await handler(message, data)


        if message.media_group_id and data.get('_is_last'):
            del self.album_data[message.media_group_id]
            del data['_is_last']











