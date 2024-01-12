from sqlalchemy import create_engine
from sqlmodel import SQLModel

DATABASE_URL = "postgresql://admin:welovetheenvironment@db/ecoact_db"
engine = create_engine(DATABASE_URL)

def create_db_and_tables() -> None:
    """
    Creates the database tables defined in SQLModel models.
    """
    SQLModel.metadata.create_all(engine)

