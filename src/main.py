from asyncio import run
from aiogram import Bot, Dispatcher
from src.Routers.communicate import FirstRouter
from connect import Connect
from botmenu import bot_commands
from Routers.PoolRouter import PoolRouter
from filters.group_media import AlbumMiddleware


class ExecuteFile:

    """По файлу понятно, что он делает"""

    @staticmethod
    async def main():

        # storage = RedisStorage.from_url(url='redis://localhost:6379/0')

        #Место для подключения других объектов
        con = Connect()  # переменная с токеном бота
        bot = Bot(con.connect())
        dp = Dispatcher()


        #Место для подключения рутеров к основному
        dp.include_router(FirstRouter.router)
        dp.include_router(PoolRouter.router)


        # Место для мидлвари
        dp.message.middleware(AlbumMiddleware())


        #Место для выдачи ответов от метода main
        await bot_commands(bot)
        await bot.delete_webhook(drop_pending_updates=True, request_timeout=100)
        await dp.start_polling(bot)





if __name__ == "__main__":
    try:
        print("Enter to Bot")
        exec = ExecuteFile()
        run(exec.main())


    except KeyboardInterrupt:
        print('Connect is interrupted by press-F')


    except Exception as e:
        print(str(e))
