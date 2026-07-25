from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Expense(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    label: str = Field(min_length=5, max_length=100)
    expense_date: str
    item_price: float
    currency: str
    amount: int
    unit: str
    category: str


class ExpenseCreate(BaseModel):
    label: str = Field(min_length=5)
    expense_date: str
    item_price: float
    currency: str
    amount: int
    unit: str
    category: str


class ExpenseUpdate(BaseModel):
    label: str | None = Field(default=None, min_length=5)
    expense_date: str | None = None
    item_price: float | None = None
    currency: str | None = None
    amount: int | None = None
    unit: str | None = None
    category: str | None = None
