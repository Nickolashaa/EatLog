from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine(url="sqlite:///src/database/database.db")
session_maker = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
