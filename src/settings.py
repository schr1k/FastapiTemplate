from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent
jwt_private_path: Path = BASE_DIR / 'src' / 'auth' / 'certs' / 'jwt_private.pem'
jwt_public_path: Path = BASE_DIR / 'src' / 'auth' / 'certs' / 'jwt_public.pem'


class Settings(BaseSettings):
    # Postgres
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # Api
    DEBUG: bool
    API_PORT: int

    # Jwt
    TOKEN_TYPE: str
    ALGORITHM: str
    EXPIRE_MINUTES: int
    JWT_PRIVATE: str = jwt_private_path.read_text()
    JWT_PUBLIC: str = jwt_public_path.read_text()

    @property
    def db_url(self) -> str:
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
