from aiogram.filters import BaseFilter
from aiogram.types import Message



class ValidEmail(BaseFilter):

    '''Создадим здесь ради практики более менее валид на почту'''


    async def __call__(self, message: Message):
        tg_name = message.text


        if "@" in tg_name and len(tg_name) >= 2:
            return True
        else:
            return False

