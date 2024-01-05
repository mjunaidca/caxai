from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv, find_dotenv
from .sqlalchemy_models import Base

_: bool = load_dotenv(find_dotenv())

DB_URL = os.environ.get("DB_URL")

if DB_URL is None:
    raise Exception("No DB_URL environment variable found")

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
