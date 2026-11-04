from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fast_zero.models import User
from fast_zero.settings import Settings
from fast_zero.settings import Settings
from fastapi import HTTPException
from http import HTTPStatus

engine = create_engine(Settings().DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session