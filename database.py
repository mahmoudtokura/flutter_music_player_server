from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:localdb:5434/dename"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
