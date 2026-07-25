from sqlmodel import Session, SQLModel, create_engine, func, select

from settings.database_settings import database_settings

# "mysql://dbadmin:adjkfha89kNN*Ljkd@databaseserver.najah.edu/demo_api_db"

engine = create_engine(
    database_settings.DATABASE_URL,
    echo=database_settings.ECHO,
    connect_args={"check_same_thread": False},
)


def create_db_tables():
    from models.books import Book  # noqa: F401
    from models.expenses import Expense  # noqa: F401

    SQLModel.metadata.create_all(bind=engine)


def seed_db():
    from models.books import Book
    from models.expenses import Expense

    with Session(bind=engine) as session:
        # Seed expenses (existing code)
        statement = select(func.count()).select_from(Expense)
        expense_count = session.exec(statement).first()
        if expense_count is None or expense_count == 0:
            session.add_all(
                [
                    Expense(
                        id=None,
                        label="Bread",
                        expense_date="2026-07-05",
                        item_price=3,
                        currency="NIS",
                        amount=1,
                        unit="KG",
                        category="food",
                    ),
                    Expense(
                        id=None,
                        label="Milk",
                        expense_date="2026-07-05",
                        item_price=5.5,
                        currency="NIS",
                        amount=2,
                        unit="Litre",
                        category="food",
                    ),
                ]
            )

        # Seed books (new code)
        book_statement = select(func.count()).select_from(Book)
        book_count = session.exec(book_statement).first()
        if book_count is None or book_count == 0:
            session.add_all(
                [
                    Book(
                        id=None,
                        title="Python",
                        author="Eric Matthes",
                        price=39.99,
                        pages=544,
                        year=2019,
                    ),
                    Book(
                        id=None,
                        title="Clean Code",
                        author="Robert Martin",
                        price=44.99,
                        pages=464,
                        year=2008,
                    ),
                ]
            )

        session.commit()
