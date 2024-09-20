from aiogram import Router
from src.FSMclasses.fsmPool import FsmPool
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import Message




class PoolRouter:

    router = Router()



@PoolRouter.router.message(F.text=='/cancel', state='*')
async def cancel_cmd(message: Message, state: FSMContext):
    '''Для сброса всех состояний'''
    current_state = await state.get_state()

    if current_state is None:
        return


    await state.clear()
    await message.answer(text="Вы вышли из опроса. К сожалению, все ваши данные не были сохранены")




