from fastapi import APIRouter, HTTPException, Path, Query, status
from sqlmodel import select

from dependencies import SessionDep
from models.books import Book, BookCreate, BookUpdate

router = APIRouter(tags=["Books"])


# GET /books - List all books
@router.get("/books")
def books_list(
    session: SessionDep,
    min_price: float | None = Query(default=None, gt=0),
):
    statement = select(Book)

    if min_price is not None:
        statement = statement.where(Book.price >= min_price)

    return session.exec(statement).all()


# GET /books/{book_id} - Get one book
@router.get("/books/{book_id}")
def books_detail(
    session: SessionDep,
    book_id: int = Path(gt=0, le=99999),
):
    statement = select(Book).where(Book.id == book_id)
    book = session.exec(statement).first()

    if book is not None:
        return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with id {book_id} not found!",
    )


# POST /books - Create a new book
@router.post("/books")
def books_create(
    session: SessionDep,
    book: BookCreate,
):
    db_book = Book(**book.model_dump())
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


# PATCH /books/{book_id} - Update a book
@router.patch("/books/{book_id}")
def books_update(
    session: SessionDep,
    book_id: int,
    book: BookUpdate,
):
    statement = select(Book).where(Book.id == book_id)
    db_book = session.exec(statement).first()

    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found!",
        )

    db_book.sqlmodel_update(book.model_dump(exclude_none=True))
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


# DELETE /books/{book_id} - Delete a book
@router.delete("/books/{book_id}")
def books_delete(
    session: SessionDep,
    book_id: int,
):
    statement = select(Book).where(Book.id == book_id)
    db_book = session.exec(statement).first()

    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found!",
        )

    session.delete(db_book)
    session.commit()
