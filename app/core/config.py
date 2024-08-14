from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    TEST_DATABASE_URL: str
    TESTING: bool
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_SENDER: str
    SMTP_PASSWORD: str
    BASE_URL: str
    VERIFICATION_TOKEN_EXPIRE_HOURS: int
    PAPERTRAIL_URL: str
    PAPERTRAIL_PORT: int

    
    class Config:
        env_file = ".env"

settings = Settings()