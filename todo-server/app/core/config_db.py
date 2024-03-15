from sqlmodel import create_engine, Session, SQLModel
from app.core import settings
from app.models import TODO

# only needed for psycopg 3 - replace postgresql
# with postgresql+psycopg in settings.DATABASE_URL
connection_string = str(settings.DB_URL).replace(
    "postgresql", "postgresql+psycopg"
)


engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
)

# Dependency with retry mechanism for OperationalError
def get_db():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
