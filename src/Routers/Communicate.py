from aiogram import Router
from aiogram.types import Message
from aiogram import F



class FirstRouter:

    '''Каждый новые router
    будет создаваться в отдельном классе.
    Так как я тренирую ООП для java'''

    router = Router()




@FirstRouter.router.message(F.text == '/start')
async def start(message: Message):
    await message.answer(text="""
    Привет, это помощник Алёны!\nЗдесь ты сможешь записаться на консультацию к ней.
    \n\nПожалуйста, заполните форму как можно подробнее, так как это поможет точно диагностирвать проблему и собрать для вас максимально прицельные инструкции.
    \n\n❗Важна каждая деталь или мелочь❗.
    \n\nОтветы плана: "я не знаю", "как вспомню", "как попало" - это ок. Главное - честность.
    \n\n<em><b><u>Заполняя форму, вы даете согласие на сбор и обработку персональных данных</u></b></em>.
    """, parse_mode='html')






