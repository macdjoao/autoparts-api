from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


# A classe BaseSettings do Pydantic já lê o arquivo .env, não sendo necessário os.getenv('ENVVAR')
class Settings(BaseSettings):
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
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ALGORITHM: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str

    @property
    def DB_URL(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        case_sensitive = True
        env_file = '.env'


settings: Settings = Settings()
