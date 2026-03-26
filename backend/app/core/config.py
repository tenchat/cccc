from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path


# 获取 backend 目录的绝对路径
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    APP_NAME: str = "就业信息分析平台"
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/employment_db"
    REDIS_URL: str = "redis://localhost:6379/0"

    MINIMAX_API_KEY: str
    MINIMAX_BASE_URL: str
    MINIMAX_MODEL: str

    class Config:
        env_file = BACKEND_DIR / ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()