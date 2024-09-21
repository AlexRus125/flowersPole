from aiogram import Router
from src.fsmclasses.fsmPool import FsmPool
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state








class PoolRouter:

    router = Router()



@PoolRouter.router.message(F.text=='/cancel', ~StateFilter(default_state) )
async def cancel_cmd(message: Message, state: FSMContext):
    '''Для сброса всех состояний'''
    current_state = await state.get_state()

    if current_state is None:
        return


    await state.clear()
    await message.answer(text="Вы вышли из опроса. К сожалению, все ваши данные не были сохранены")




@PoolRouter.router.message(F.text == '/start_polling', StateFilter(default_state))
async def polling(message: Message, state: FSMContext):
    await message.answer(text="""
    Отлично, начнем!\n
Хотим еще раз предупредить вас о том, что данные никому не передаются...\n
<b>А так же, для вашего же удобства, вводите корректные данные</b>
    """, parse_mode='html')

    await state.set_state(FsmPool.email_address)

    await message.answer('Введите пожалуйста ваш email-адрес')



@PoolRouter.router.message(StateFilter(FsmPool.email_address), F.text, ~F.in_(['photo', 'video', 'document', 'voice', 'sticker']))
async def get_email(message: Message, state: FSMContext):


    #
    #
    await message.answer('Спасибо, перейдем дальше')
    await message.reply(f'Учтите, что если вы захотите поменять почту, вам нужно будет пройти опрос заново')

    await state.update_data(email_address=message.text)

    await message.answer(text='Теперь нам потребуется название вашего растения(если вы его знаете)\n\n'
                              'Даже если вы не знаете, ничего страшного, просто ответье честно "не знаю"\n\n'
                              'Наши специалисты узнают сами')
    await state.set_state(FsmPool.name_plant)

@PoolRouter.router.message(StateFilter(FsmPool.name_plant), F.text)
async def get_name_plant(message: Message, state: FSMContext):

    await message.answer('Благодарим')







