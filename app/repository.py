from typing import Generator

from sqlmodel import Session, SQLModel, create_engine, select

from model import Product, ProductCreate, ProductUpdate
from settings import settings


engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def init_db() -> None:
    SQLModel.metadata.create_all(engine)

