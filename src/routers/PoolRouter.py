from aiogram import Router
from src.fsmclasses.fsmPool import FsmPool
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from src.filters.valid_email import ValidEmail




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
async def start_polling(message: Message, state: FSMContext):
    await message.answer(text="""
    Отлично, начнем!
    \nХотим еще раз предупредить вас о том, что данные никому не передаются...
    \n<b>А так же, для вашего же удобства, вводите корректные данные</b>
    """, parse_mode='html')

    await state.set_state(FsmPool.email_address)

    await message.answer('Введите пожалуйста ваш email-адрес')



@PoolRouter.router.message(ValidEmail(), StateFilter(FsmPool.email_address))
async def get_email(message: Message, state: FSMContext):


    #
    #
    await message.answer(f'Спасибо! Убедитесь, что <b>"{message.text}"</b> ваша верная почта', parse_mode='html')
    # await message.reply(f'Учтите, что если вы захотите поменять почту, вам нужно будет пройти опрос заново')

    await state.update_data(email_address=message.text)

    await message.answer(text='Теперь нам потребуется название вашего растения(если вы его знаете)\n'
                              'Даже если вы не знаете, ничего страшного, просто ответье честно "не знаю"\n'
                              'Наши специалисты узнают сами')
    await state.set_state(FsmPool.name_plant)

@PoolRouter.router.message(F.text, StateFilter(FsmPool.name_plant))
async def get_name_plant(message: Message, state: FSMContext):

    await message.answer("Очень хорошо, теперь мы перейдем к следующему вопросу")
    await state.update_data(name_plant=message.text)

    await message.answer("Опишите проблему, с которой вам нужна помощь или задайте вопрос в свободной форме")
    await state.set_state(FsmPool.problem_question)




@PoolRouter.router.message(StateFilter(FsmPool.problem_question))
async def get_problem_question(message: Message, state: FSMContext):

    await message.answer("Отлично, ваш ответ принят")
    await state.update_data(problem_question=message.text)

    await message.answer('Теперь мы хотим узнать: пробовали ли вы самостоятельно решить проблему? '
                         '\nЕсли да - расскажите, какие препараты вы использовали'
                         '\n\n<b><u>Важно!:</u></b> укажите название препарата, дозировку, срок годности при наличии и когда применяли', parse_mode='html')


    await state.set_state(FsmPool.self_solving_problem)



@PoolRouter.router.message(FsmPool.self_solving_problem)
async def get_solve(message: Message, state: FSMContext):

    await message.answer('Спасибо, вы прислали нам самостоятельное решение')
    await state.update_data(self_solving=message.text)
    await message.answer('Как часто вы поливаете ваше растение?'
                         '\nПо каким параметрам понимаете, что пора поливать?'
                         '\nЕсли вносите удобрения - напишите название, дозировки и как часто добавляете')
    await state.set_state(FsmPool.watering_frequency)




@PoolRouter.router.message(FsmPool.watering_frequency)
async def get_watering(message: Message, state: FSMContext):

    await message.answer(f'Хорошо, идем дальше')
    await state.update_data(watering=message.text)
    await message.answer('Есть ли в горшке, где находится растение, дренажное отверстие?')
    await state.set_state(FsmPool.hole_true)



@PoolRouter.router.message(FsmPool.hole_true)
async def get_hole_true(message: Message, state: FSMContext):

    await message.answer('Принято')
    await state.update_data(hole_true=message.text)
    await message.answer('Как давно вы пересаживали растение?'
                         '\nКакой грунт использовали? Если были разрыхлители, укажите название')

    await state.set_state(FsmPool.transplantation)





@PoolRouter.router.message(FsmPool.transplantation)
async def get_trans(message: Message, state: FSMContext):

    await message.answer('Спасибо')
    await state.update_data(trans=message.text)
    # await cancel_cmd
    # await state.set_state(None)
    await state.clear()
    await message.answer('Опрос закончился')