from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class FsmPool(StatesGroup):
    '''Класс для текстового опроса'''
    #Первый скриншот
    tg_name = State()
    name_plant = State()
    problem_question = State()
    #Второй скриншот

    self_solving_problem = State()
    watering_frequency = State()
    hole_true = State()
    transplantation = State()
    #Третий скриншот

    """..."""


    #Четвертый скриншот


class FSMImages(StatesGroup):
    '''главный класс для обработки фоток'''

    image1 = State()
    image2 = State()
    image3 = State()
    image4 = State()
    image5 = State()
    image6 = State()
    image7 = State()
    image8 = State()


