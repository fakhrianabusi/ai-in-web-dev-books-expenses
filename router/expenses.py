from fastapi import APIRouter, HTTPException, Path, Query, status
from sqlmodel import select

from dependencies import SessionDep
from models.expenses import Expense, ExpenseCreate, ExpenseUpdate

router = APIRouter(tags=["Expenses"])


@router.get("/expenses")
def expenses_list(
    # min_price: float | None = None,
    session: SessionDep,
    min_price: float | None = Query(default=None, gt=0),
):
    statement = select(Expense)
    if min_price is not None:
        statement = select(Expense).where(Expense.item_price >= min_price)
    return session.exec(statement).all()
    # pagination !!!!!   limit (50 item)      skip (start point)


@router.get("/expenses/{id}")
def expenses_detail(
    session: SessionDep,
    id: int = Path(gt=0, le=99999),
):
    statement = select(Expense).where(Expense.id == id)
    expense = session.exec(statement).first()
    if expense is not None:
        return expense

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Expense with id {id} not found!"
    )


@router.post("/expenses")
def expenses_create(
    session: SessionDep,
    expense: ExpenseCreate,
):
    db_expense = Expense(**expense.model_dump())
    session.add(db_expense)
    session.commit()
    session.refresh(db_expense)
    return db_expense


@router.patch("/expenses/{id}")
def expenses_update(
    session: SessionDep,
    id: int,
    expense: ExpenseUpdate,
):
    # select the expense from database
    statement = select(Expense).where(Expense.id == id)
    db_expense = session.exec(statement).first()
    # raise exception if expense not exist
    if db_expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {id} not found!",
        )

    db_expense.sqlmodel_update(expense.model_dump(exclude_none=True))
    session.add(db_expense)
    session.commit()
    session.refresh(db_expense)
    return db_expense


@router.delete("/expenses/{id}")
def expenses_delete(
    id: int,
    session: SessionDep,
):
    # Prepare commands
    # select the expense from database
    statement = select(Expense).where(Expense.id == id)
    db_expense = session.exec(statement).first()
    # raise exception if expense not exist
    if db_expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {id} not found!",
        )
    session.delete(db_expense)
    session.commit()


# def dump_function(id, name):
#     pass
# dump_function(id=1, name="Ahmad")
# user = {"id": 1, "name": "Ahmad"}
# dump_function(id=user["id"], name=user["name"])
# dump_function(**user)
