from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from app.core.config import settings 

# PostgreSQL engine - remove echo=True for production
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={
        "options": "-c timezone=utc"
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    import app.models  
    Base.metadata.create_all(bind=engine)