from asyncio import run
from aiogram import Bot, Dispatcher
from src.routers.communicate import FirstRouter
from connect import Connect
from botmenu import bot_commands
from routers.PoolRouter import PoolRouter
from aiogram.fsm.storage.redis import RedisStorage




class ExecuteFile:

    """По файлу понятно, что он делает"""

    @staticmethod
    async def main():

        storage = RedisStorage.from_url(url='redis://localhost:6379/0')

        #Место для подключения других объектов
        con = Connect()  # переменная с токеном бота
        bot = Bot(con.connect())
        dp = Dispatcher(storage=storage)

        #Место для подключения рутеров к основному
        dp.include_router(FirstRouter.router)
        dp.include_router(PoolRouter.router)

        #Место для выдачи ответов от метода main
        await bot_commands(bot)
        await bot.delete_webhook(drop_pending_updates=True, request_timeout=1080)
        await dp.start_polling(bot)





if __name__ == "__main__":
    try:
        print("Enter to Bot")
        exec = ExecuteFile()
        run(exec.main())


    except KeyboardInterrupt:
        print('Connect is interrupted by CTRL+C')


    except Exception as e:
        print(str(e))
