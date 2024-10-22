from aiogram import Router
from src.fsmclasses.fsmPool import FsmPool
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import Message, InputMediaVideo, ReplyKeyboardRemove
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from src.filters.valid_email import ValidEmail
from aiogram import Bot
from aiogram.types import ContentType as CT
from aiogram.types.input_media import InputMedia
from aiogram.types import InputMediaPhoto
from src.fsmclasses.fsmReport import FsmReport
from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardMarkup





class PoolRouter:

    router = Router()


@PoolRouter.router.message(StateFilter(default_state), F.text=='/report')
async def report(message: Message, bot: Bot, state: FSMContext):

    await message.answer("Данное действие позволяет нам улучшать бота в соответствии с вашими интересами."
                         "\nНапишите, что бы вы хотели улучшить в боте, можете отправить нам фотографию с текстом или написать обычным текстом")
    await state.set_state(FsmReport.sending)

#
# @PoolRouter.router.message(StateFilter(FsmReport.sending), F.content_type.in_([CT.PHOTO, CT.TEXT]))
# async def send_report(message: Message, bot: Bot, state: FSMContext):
#     if message.photo:
#         await bot.send_photo(chat_id=1041131470, photo=message.photo[-1].file_id)
#
#     elif message.text:
#         await bot.send_message(chat_id=1041131470, text=message.text)
#
#     await message.reply('Благодарим вас за ваш вклад в работу бота!')
#     await state.clear()



# @PoolRouter.router.message(F.text=='/cancel', ~StateFilter(default_state) )
# async def cancel_cmd(message: Message, state: FSMContext):
#     '''Для сброса всех состояний'''
#     current_state = await state.get_state()
#
#     if current_state is None:
#         return
#
#
#     await state.clear()
#     await message.answer(text="Вы вышли из опроса. К сожалению, все ваши данные не были сохранены")


@PoolRouter.router.message(F.text == '/start_polling', StateFilter(default_state))
async def start_polling(message: Message, state: FSMContext):
    # await state.update_data(tg_user=message.from_user.username)
    await state.clear()


    buttons = [
        [KeyboardButton(text=f"@{message.from_user.username}")],
    ]
    kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)

    await message.answer('Отправьте нам ваш никнейм в телеграмме'
                         '\nНужно нажать на появившуюся кнопку снизу', reply_markup=kb)
    await state.set_state(FsmPool.tg_name)

    # await state.set_state(FsmPool.name_plant)
@PoolRouter.router.message(F.text, StateFilter(FsmPool.tg_name), ValidEmail())
async def get_email(message: Message, state: FSMContext):
    await message.answer('1/8'
                         '\nНазвание растения'
                         '\n[ если не знаете, ставьте "0"]', reply_markup=ReplyKeyboardRemove(), parse_mode='MarkdownV2')
    await state.update_data(tg_name=message.text)

    await state.set_state(FsmPool.name_plant)




@PoolRouter.router.message(F.text, StateFilter(FsmPool.name_plant))
async def get_name_plant(message: Message, state: FSMContext):

    await state.update_data(name_plant=message.text)

    await message.answer("2/8"
                         "\nОпишите проблему своими словами")
    await state.set_state(FsmPool.problem_question)




@PoolRouter.router.message(F.text, StateFilter(FsmPool.problem_question))
async def get_problem_question(message: Message, state: FSMContext):

    await state.update_data(problem_question=message.text)

    await message.answer('3/8'
                         '\nЕсли вы пробовали решить ее самостоятельно или'
                         '\nлечить растение, расскажите, что делали.'
                         '\n[если нет, ставьте "0"]')


    await state.set_state(FsmPool.self_solving_problem)



@PoolRouter.router.message(F.text, StateFilter(FsmPool.self_solving_problem))
async def get_solve(message: Message, state: FSMContext):

    await state.update_data(self_solving=message.text)
    await message.answer("4/8"
                         "\nКак часто поливаете?"
                         "\nПо каким параметрам понимаете, что пора поливать?"
                         "\nЕсли вносите удобрения - напишите название,"
                         "\nдозировки и как часто добавляете.")
    await state.set_state(FsmPool.watering_frequency)




@PoolRouter.router.message(F.text, StateFilter(FsmPool.watering_frequency))
async def get_watering(message: Message, state: FSMContext):


    await state.update_data(watering=message.text)
    await message.answer('5/8'
                         '\nЕсть ли в горшке дренажное отверстие?')
    await state.set_state(FsmPool.hole_true)



@PoolRouter.router.message(F.text, StateFilter(FsmPool.hole_true))
async def get_hole_true(message: Message, state: FSMContext):


    await state.update_data(hole_true=message.text)
    await message.answer('6/8'
                         '\nКак давно вы пересаживали растение?'
                         '\nКакой грунт использовали? '
                         '\nЕсли были разрыхлители, укажите название.')

    await state.set_state(FsmPool.transplantation)


@PoolRouter.router.message(F.text, StateFilter(FsmPool.transplantation))
async def get_win_and_floor(message: Message, state: FSMContext):
    await state.update_data(trans=message.text)
    await message.answer('7/8'
                         '\nЕсть ли напротив ближайшего к растению окна'
                         '\nздания или деревья?'
                         '\nНа каком этаже помещение?')
    await state.set_state(FsmPool.win_and_floor)


@PoolRouter.router.message(F.text, StateFilter(FsmPool.win_and_floor))
async def get_some_imp(message: Message, state: FSMContext):

    await state.update_data(win_and_floor=message.text)
    await message.answer('8/8'
                         '\nЕсли есть что-то еще, о чем вы считаете важным'
                         '\nупомянуть - напишите это')

    await state.set_state(FsmPool.some_important)



@PoolRouter.router.message(F.text, StateFilter(FsmPool.some_important))
async def get_some_imp(message: Message, bot: Bot, state: FSMContext):

    '''#! Заключительный рутер перед отправкой фоток или видео #!'''
    await state.update_data(some_important=message.text)

    await message.answer('Спасибо!'
                         '\nСейчас нужно будет последовательно сделать'
                         '\nнесколько снимков.'
                         '\nМинимум 8, но можно и больше.'
                         '\nВы можете отправить как фотографии, так и видео для каждого пункта.'
                         '\nЧем более четкие и яркие фотографии крупных'
                         '\nпланов - тем более точно мы сможем'
                         '\nдиагностировать проблему.')

    await message.answer('''
    1.8 Общие планы растения сбоку, чтобы было видно горшок
    \n2.8 Общий план растения сверху, чтобы было видно грунт
    \n3.8 Грунт крупным планом
    \n4.8 Крупный план листа с обратной стороны
    \n5.8 Крупный план соединения листа и стебля(если такое есть)
    \n6.8 Общий план помещения, чтобы было видно растение
    \n7.8 Вид из окна, ближайшего к растению
    \n8.8 Если рядом с растением есть приборы отопления или кондиционер, то сделайте кадр так, чтобы их было видно
    
    \n<b><em>Просим вас прислать все фотографии или видео одной общей группой, а не по отдельности каждое, иначе вам придется проходить опрос заново</em></b>''', parse_mode='html')

    await state.set_state(FsmPool.final_state)


#! Самый важный рутер
@PoolRouter.router.message(StateFilter(FsmPool.final_state), F.content_type.in_([CT.PHOTO, CT.VIDEO]))
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


    await bot.send_media_group(chat_id=6175927940, media=media_group)  #33626334
    await bot.send_message(chat_id=6175927940,
        text=f'''
        Ник в телеграмме - {data["tg_name"]}
        \n1/8) {data["name_plant"]}
        \n2/8) {data["problem_question"]}
        \n3/8) {data["self_solving"]}
        \n4/8) {data["watering"]}
        \n5/8) {data["hole_true"]}
        \n6/8) {data["trans"]}
        \n7/8) {data["win_and_floor"]}
        \n8/8) {data["some_important"]}''')

    await bot.send_message(message.chat.id,
                           text='Спасибо, вы прекрасны!'
                                '\nМы получили ваше сообщение'
                                '\nВ течение двух рабочих дней мы пришлем вам одним сообщением'
                                '\nрезультаты диагностики и рекомендации по дальнейшим действиям.'
                                '\nА пока приглашаем вас в наш телеграмм-канал,'
                                '\nтам мы раскрываем секреты красивых растений и рассказываем о внутренней кухне Третьего Дня.'
                                '\n\n<b>p.s. сейчас бот в стадии тестирования, поэтому оплата консультации по желанию и согласно той ценности, которую вы для себя определите сами. Cсылка будет в нашем сообщении с диагностикой и рекомендациями.</b>'
                                '\n<b>p.p.s. если у вас есть идеи по улучшению этого брифа, пожалуйста напишите нам на <a href="https://t.me/thrdday_person">thrdday_person</a></b>',
                           parse_mode='html')

    await state.clear()









