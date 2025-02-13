
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = getenv('PROJECT_NAME')
    SECRET_KEY: str = getenv('SECRET_KEY')
    ALGORITHM: str = getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

settings = Settings()
