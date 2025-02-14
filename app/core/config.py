
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = getenv('PROJECT_NAME')
    SECRET_KEY: str = getenv('SECRET_KEY')
    ALGORITHM: str = getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    DIFY_API_KEY: str = getenv('DIFY_API_KEY')
    DIFY_API_URL: str = getenv('DIFY_API_URL')
    USER_NAME: str = getenv('USER_NAME')
    USER_EMAIL: str = getenv('USER_EMAIL')
    USER_FULLNAME: str = getenv('USER_FULLNAME')
    USER_PASSWORD: str = getenv('USER_PASSWORD')

settings = Settings()
