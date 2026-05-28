import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file explicitly
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "athiyaman")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
    DB_DRIVER: str = os.getenv("DB_DRIVER", "postgresql")

    # Security Configuration
    JWT_SECRET: str = os.getenv(
        "JWT_SECRET", "428f8f2b7405e32a673c6a49db21cd197c36a4b12c3f4e5a6b7c8d9e0f1a2b3c"
    )
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    REFERRAL_EXPIRY_HOURS: int = int(os.getenv("REFERRAL_EXPIRY_HOURS", "72"))

    # Storage Configuration
    STORAGE_TYPE: str = os.getenv("STORAGE_TYPE", "LOCAL")
    STORAGE_PATH: str = os.getenv("STORAGE_PATH", "d:\\Athiyaman\\uploads")

    # External API Configuration
    INDIA_POST_API_URL: str = os.getenv("INDIA_POST_API_URL", "https://api.postalpincode.in/pincode/")

    @property
    def DATABASE_URL(self) -> str:
        # Standard SQLAlchemy connection string
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
