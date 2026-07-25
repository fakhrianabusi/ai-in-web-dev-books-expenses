from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from database import engine


def create_session():
    with Session(bind=engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(create_session)]
