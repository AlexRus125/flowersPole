from environs import Env




class Connect:
    """Для подключения переменной виртуального окружения"""

    @staticmethod
    def connect(path: str | None = None):
        env = Env()
        env.read_env(path)


        return env('BOT_TOKEN')





