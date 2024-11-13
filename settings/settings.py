from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


# A classe BaseSettings do Pydantic já lê o arquivo .env, não sendo necessário os.getenv('ENVVAR')
class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file='.env')

    APP: str = 'main:app'
    APP_VERSION: str
    APP_HOST: str
    APP_PORT: int
    APP_RELOAD: bool
    URI_PREFIX: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 1 * 1  # (minutos * horas * dias)
    ALGORITHM: str
    SECRET_KEY: str

    @property
    def DB_URL(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings: Settings = Settings()
