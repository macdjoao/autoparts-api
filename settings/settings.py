import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    APP: str = 'main:app'
    APP_VERSION: str = str(os.getenv('APP_VERSION'))
    APP_HOST: str = str(os.getenv('APP_HOST'))
    APP_PORT: str = int(os.getenv('APP_PORT'))
    APP_RELOAD: bool = eval(os.getenv('APP_RELOAD'))
    URI_PREFIX: str = str(os.getenv('URI_PREFIX'))

    class Config:
        case_sensitive = True
        env_file = '.env'


settings: Settings = Settings()
