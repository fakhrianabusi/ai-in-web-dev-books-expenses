from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    pages: int | None = Field(default=None, gt=0)
    year: int | None = Field(default=None, gt=1000, le=2100)


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    pages: int | None = Field(default=None, gt=0)
    year: int | None = Field(default=None, gt=1000, le=2100)


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    author: str | None = Field(default=None, min_length=1, max_length=100)
    price: float | None = Field(default=None, gt=0)
    pages: int | None = Field(default=None, gt=0)
    year: int | None = Field(default=None, gt=1000, le=2100)
