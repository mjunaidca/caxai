from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.exc import SQLAlchemyError

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
    except SQLAlchemyError as e:
        # Log the error for debugging purposes
        print(f"Database error occurred: {e}")
        # Depending on your application's needs, you might want to handle the error
        # differently, such as rolling back the transaction or re-raising the error.
    finally:
        db.close()
