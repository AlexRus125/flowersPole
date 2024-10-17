from aiogram import Router
from src.fsmclasses.fsmPool import FsmPool
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import Message, InputMediaVideo
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from src.filters.valid_email import ValidEmail
from aiogram import Bot
from aiogram.types import ContentType as CT
from aiogram.types.input_media import InputMedia
from aiogram.types import InputMediaPhoto
from src.fsmclasses.fsmReport import FsmReport





class PoolRouter:

    router = Router()


@PoolRouter.router.message(StateFilter(default_state), F.text=='/report')
async def report(message: Message, bot: Bot, state: FSMContext):

    await message.answer("Данное действие позволяет нам улучшать бота в соответствии с вашими интересами."
                         "\nНапишите, что бы вы хотели улучшить в боте, можете отправить нам фотографию с текстом или написать обычным текстом")
    await state.set_state(FsmReport.sending)


@PoolRouter.router.message(StateFilter(FsmReport.sending), F.content_type.in_([CT.PHOTO, CT.TEXT]))
async def send_report(message: Message, bot: Bot, state: FSMContext):
    if message.photo:
        await bot.send_photo(chat_id=1041131470, photo=message.photo[-1].file_id)

    elif message.text:
        await bot.send_message(chat_id=1041131470, text=message.text)

    await message.reply('Благодарим вас за ваш вклад в работу бота!')
    await state.clear()



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
    \n<b>Просим вас, для нашего удобства, вводите свои корректные данные!</b>
    """, parse_mode='html')

    await state.set_state(FsmPool.tg_name)

    await message.answer('Введите пожалуйста ваш никнейм в телеграм через @ пример -> @GoToGym_', parse_mode='html')



@PoolRouter.router.message(StateFilter(FsmPool.tg_name), ValidEmail())
async def get_email(message: Message, state: FSMContext):


    #
    #
    await message.answer(f'Спасибо! Убедитесь, что <b>"{message.text}"</b> ваш никнейм в телеграмме', parse_mode='html')
    # await message.reply(f'Учтите, что если вы захотите поменять почту, вам нужно будет пройти опрос заново')

    await state.update_data(tg_name=message.text)

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
    await message.answer('Следущий вопрос'
                         '\nКак часто вы поливаете ваше растение?'
                         '\nПо каким параметрам понимаете, что пора поливать?'
                         '\n(Если вносите удобрения - напишите название, дозировки и как часто добавляете)')
    await state.set_state(FsmPool.watering_frequency)




@PoolRouter.router.message(StateFilter(FsmPool.watering_frequency))
async def get_watering(message: Message, state: FSMContext):

    await message.answer(f'Хорошо, следующий вопрос')
    await state.update_data(watering=message.text)
    await message.answer('Есть ли в горшке, где находится растение, дренажное отверстие?')
    await state.set_state(FsmPool.hole_true)



@PoolRouter.router.message(StateFilter(FsmPool.hole_true))
async def get_hole_true(message: Message, state: FSMContext):

    await message.answer('Принято')
    await state.update_data(hole_true=message.text)
    await message.answer('Как давно вы пересаживали растение?'
                         '\nКакой грунт использовали? Если были разрыхлители, укажите название(если не было, можно ничего не писать)')

    await state.set_state(FsmPool.transplantation)





@PoolRouter.router.message(StateFilter(FsmPool.transplantation))
async def get_trans(message: Message, bot: Bot, state: FSMContext):

    '''#! Заключительный рутер перед отправкой фоток или видео #!'''


    await message.answer('Спасибо!')
    await message.answer('Подготовьте фото | видео, чтобы могли проанализировать вашу проблему')
    await message.answer('''
    1.8 Общие планы растения, чтобы было видно горшок
    \n2.8 Общий план растения сверху, чтобы было видно грунт
    \n3.8 Крупные планы, чтобы видны листья с лицевой стороны
    \n4.8 Крупные планы, чтобы были видны листья с изнаночной стороны
    \n5.8 Крупные планы, чтобы были видны соединения листа и стебля(если такое есть)
    \n6.8 Общий план растения в комнате
    \n7.8 Вид из окна, ближайшего к растению
    \n8.8 Если рядом с растением есть приборы отопления или кондиционер, то сделайте кадр так, чтобы их было видно
    
    \n<b><em>Данная инструкция написана только для того, чтобы показать то, что надо прислать нам. Вам не нужно расставлять каждую цифру под соответствуйщей фоткой</em></b>''', parse_mode='html')
    await state.update_data(trans=message.text)
    await state.set_state(default_state)


#! Самый важный рутер
@PoolRouter.router.message(F.content_type.in_([CT.PHOTO, CT.VIDEO]), StateFilter(None))
async def handle_message(message: Message, album: list[Message], bot: Bot, state: FSMContext):
    #В каждом хэндлере первым параметром идет event -> то, что придет в хэндлер
    #Вторым параметром идет data -> то, чем нужно ответить.
    #Потом *args и **kwargs


    media_group = []

    for msg in album:
        if msg.photo:
            file_id = msg.photo[-1].file_id
            media_group.append(InputMediaPhoto(media=file_id))

        elif msg.video:

            file_id = msg.video.file_id
            media_group.append(InputMediaVideo(media=file_id))


        else:
            obj_dict = msg.dict()
            file_id = obj_dict[msg.content_type]['file_id']
            media_group.append(InputMedia(media=file_id))


    data = await state.get_data()


    await bot.send_media_group(chat_id=1041131470, media=media_group)
    await bot.send_message(chat_id=1041131470,
        text=f'''
        1){data["tg_name"]}\n2){data["name_plant"]}\n3){data["problem_question"]}\n4){data["self_solving"]}\n5){data["watering"]}\n6){data["hole_true"]}\n7){data["trans"]}''')

    await bot.send_message(message.chat.id, text='Спасибо за ваши ответы, мы получили их и начали готовить решение.')

    await state.clear()