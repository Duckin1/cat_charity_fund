from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'PRACTICUM'
    description: str = 'Многопользовательская система, основанная на принципах асинхронности'

    class Config:
        env_file = '.env'


settings = Settings()
