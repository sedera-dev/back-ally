import os
import environ

env = environ.Env()
environ.Env.read_env()

class Settings:
    PROJECT_NAME: str = env('PROJECT_NAME')
    SECRET_KEY: str = env('SECRET_KEY')
    ALGORITHM: str = env('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = env('ACCESS_TOKEN_EXPIRE_MINUTES')

settings = Settings()
