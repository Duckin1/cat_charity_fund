from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд поддержки котиков QRKot'
    app_description: str = 'Помогаем котикам'
    database_url: str = 'sqlite+aiosqlite:///./qr_cat.db'
    secret: str = 'SECRET'
    token_lifetime = 3600

    class Config:
        env_file = '.env'


settings = Settings()
