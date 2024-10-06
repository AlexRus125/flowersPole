from aiogram.filters import BaseFilter
from aiogram.types import Message



class ValidEmail(BaseFilter):

    '''Создадим здесь ради практики более менее валид на почту'''


    async def __call__(self, message: Message):
        email = message.text


        if "@" in email and '.' in email and len(email) >= 2:
            return True
        else:
            return False

