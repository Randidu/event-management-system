import os
from dotenv import load_dotenv
from urllib.parse import quote_plus


load_dotenv()

class Settings:
    PROJECT_NAME: str = "EMS Backend"   
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Backend API for EMS system"

    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "Rana@2006")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "EMS_DB")


    SQLALCHEMY_DATABASE_URL: str = (
        f"postgresql+psycopg2://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()