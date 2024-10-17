from aiogram.types import BotCommand
from aiogram import Bot
from aiogram.types import BotCommandScopeDefault


async def bot_commands(bot: Bot):
    commands = [
        BotCommand(command='/start',
                   description='Общая информация бота'),

        BotCommand(command='/start_polling',
                   description='Начать опрос'),

        BotCommand(command='/cancel',
                   description='Прекратить опрос'),

        BotCommand(command='/report',
                   description='Ваши предложения, что бы вы хотели добавить'),
    ]

    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
