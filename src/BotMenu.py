from aiogram.types import BotCommand
from aiogram import Bot


async def bot_commands(bot: Bot):

    commands = [
    BotCommand(command='/start',
               description='Начать работку'),

    BotCommand(command='/start_pooling',
               description='Начать опрос'),

    BotCommand(command='/cancel',
               description='Прекратить опрос')
    ]


    await bot.set_my_commands(commands)



