from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# arquivo local insights.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./insights.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# dependência para injetar o banco nas rotas do FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()