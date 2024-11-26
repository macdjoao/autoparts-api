from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


# A classe BaseSettings do Pydantic já lê o arquivo .env, não sendo necessário os.getenv('ENVVAR')
class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file='.env')

    # Framework
    APP: str = 'main:app'
    APP_VERSION: str
    APP_HOST: str
    APP_PORT: int
    APP_RELOAD: bool
    URI_PREFIX: str

    # Database
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    # JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # (minutos * horas * dias)
    ALGORITHM: str
    SECRET_KEY: str

    # Admin
    CREATE_ADMIN: bool
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str

    # Cache
    CACHE_HOST: str
    CACHE_PORT: int = 6379
    CACHE_DB: int
    CACHE_TIME_TO_EXP: int = 60 * 60 * 1  # (segundos * minutos * horas)

    @property
    def DB_URL(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings: Settings = Settings()
