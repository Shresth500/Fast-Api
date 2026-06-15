from sqlmodel import create_engine, SQLModel, Session
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_FILE_NAME = os.getenv("DATABASE_FILE_NAME")
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = f"{DATABASE_URL}:///{DATABASE_FILE_NAME}"
                         


sqlite_file_name = DATABASE_FILE_NAME
sqlite_url = f"{DATABASE_URL}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session