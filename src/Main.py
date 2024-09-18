from asyncio import run
from aiogram import Bot, Dispatcher
from src.Routers.Communicate import FirstRouter
from Connect import Connect

class ExecuteFile:

    """По файлу понятно, что он делает"""

    @staticmethod
    async def main():

        #Место для подключения других объектов
        con = Connect()  # переменная с токеном бота
        bot = Bot(con.connect())
        dp = Dispatcher()

        #Место для подключения рутеров к основному
        dp.include_router(FirstRouter.router)


        #Место для выдачи ответов от метода main
        await bot.delete_webhook(drop_pending_updates=True)
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
