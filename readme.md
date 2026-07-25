# FastAPI Expenses and Books Tutorial

This project demonstrates building RESTful APIs with FastAPI, SQLModel, and SQLite.
It includes two complete CRUD APIs: one for managing expenses and one for managing books.
The project demonstrates application settings, dependency injection, database tables,
startup data, request validation, and CRUD operations.

## Project Structure

```text
.
├── main.py                       # FastAPI application and startup lifecycle
├── database.py                   # Database engine, table creation, and seed data
├── dependencies.py               # Per-request database session dependency
├── models/
│   ├── expenses.py               # Expense SQLModel table and request models
│   └── books.py                  # Book SQLModel table and request models
├── router/
│   ├── expenses.py               # Expense CRUD endpoints
│   └── books.py                  # Book CRUD endpoints
├── settings/
│   ├── database_settings.py      # Database configuration
│   └── general_settings.py       # Application title and version
├── .env.example                  # Example environment variables
└── requirements.txt              # Python dependencies
```

## Environment Setup on Windows

The commands below use **Windows Command Prompt**, not PowerShell or Git Bash.
Open the project folder in VS Code and select **Command Prompt** as the terminal
profile, or open Command Prompt from the Windows Start menu.

### 1. Install Python

Download and install Python from
[python.org/downloads](https://www.python.org/downloads/), then verify the
installation:

```cmd
python --version
```

### 2. Open the Project Folder

Move to the folder that contains this project:

```cmd
cd C:\path\to\tutorial
```

Replace `C:\path\to\tutorial` with the project's actual location.

### 3. Create and Activate a Virtual Environment

```cmd
python -m venv .venv
.venv\Scripts\activate
```

After activation, `(.venv)` should appear at the beginning of the Command
Prompt line. Activate the environment again whenever you open a new terminal.

### 4. Install the Requirements

Install all packages used by the project from `requirements.txt`:

```cmd
pip install -r requirements.txt
```

The requirements include FastAPI, SQLModel, and Pydantic Settings.

### 5. Configure Environment Variables

Create a local `.env` file from the included example:

```cmd
copy .env.example .env
```

The default configuration is:

```dotenv
APP_TITLE=FastAPI Demo
VERSION=0.1.0

DATABASE_URL=sqlite:///store.db
ECHO=True
```

- `APP_TITLE` and `VERSION` appear in the generated API documentation.
- `DATABASE_URL` selects the database. The default creates `store.db` in the
  project folder.
- `ECHO=True` prints generated SQL statements in the terminal.

The local `.env` file is ignored by Git so machine-specific settings and
secrets are not committed.

## Running the Application

Start the development server:

```cmd
uvicorn main:app --reload
```

If the `uvicorn` command is not available in a fresh environment, install the
FastAPI standard extras and run the command again:

```cmd
pip install "fastapi[standard]"
```

The application is available at:

```text
http://127.0.0.1:8000
```

Useful URLs:

- Root endpoint: `http://127.0.0.1:8000/`
- Interactive Swagger documentation: `http://127.0.0.1:8000/docs`
- ReDoc documentation: `http://127.0.0.1:8000/redoc`

On startup, the application creates both database tables if they do not exist.
If the tables are empty, it adds example data:
- 2 sample expenses (Bread and Milk)
- 2 sample books (Python and Clean Code)

Existing data is left unchanged.

## Data Models

### Expenses

Expenses are stored in the `Expense` SQLModel table with these fields:

| Field | Type | Notes |
| --- | --- | --- |
| `id` | integer | Generated primary key |
| `label` | string | Between 5 and 100 characters |
| `expense_date` | string | Required |
| `item_price` | number | Required |
| `currency` | string | Required |
| `amount` | integer | Required |
| `unit` | string | Required |
| `category` | string | Required |

`ExpenseCreate` validates new expense request bodies. `ExpenseUpdate` makes
every field optional so clients can update only selected values.

### Books

Books are stored in the `Book` SQLModel table with these fields:

| Field | Type | Notes |
| --- | --- | --- |
| `id` | integer | Generated primary key |
| `title` | string | Between 1 and 200 characters |
| `author` | string | Between 1 and 100 characters |
| `price` | float | Must be greater than 0 |
| `pages` | integer | Optional, must be greater than 0 |
| `year` | integer | Optional, between 1000 and 2100 |

`BookCreate` validates new book request bodies. `BookUpdate` makes every field
optional so clients can update only selected values.

## API Endpoints

### `GET /`

Returns a simple health-check-style response:

```json
{
  "Hello": "World"
}
```

### Expense Endpoints

#### `GET /expenses`

Returns every expense stored in the database.

An optional positive `min_price` query parameter filters expenses whose
`item_price` is greater than or equal to the supplied value:

```text
GET /expenses?min_price=4
```

#### `GET /expenses/{id}`

Returns one expense by ID:

```text
GET /expenses/1
```

The ID must be between `1` and `99999`. A missing expense returns
`404 Not Found`.

#### `POST /expenses`

Creates and returns a new expense:

```json
{
  "label": "Apples",
  "expense_date": "2026-07-18",
  "item_price": 4.5,
  "currency": "NIS",
  "amount": 2,
  "unit": "KG",
  "category": "food"
}
```

The database generates the expense ID.

#### `PATCH /expenses/{id}`

Updates and returns an existing expense. Send only the fields that should
change:

```json
{
  "item_price": 4,
  "amount": 2
}
```

A missing expense returns `404 Not Found`.

#### `DELETE /expenses/{id}`

Deletes an expense:

```text
DELETE /expenses/1
```

A missing expense returns `404 Not Found`.

### Book Endpoints

#### `GET /books`

Returns every book stored in the database.

Optional query parameters:
- `min_price`: Filter books with price greater than or equal to this value
- `author`: Filter books by author name

```text
GET /books?min_price=40
GET /books?author=Eric Matthes
```

#### `GET /books/{book_id}`

Returns one book by ID:

```text
GET /books/1
```

The ID must be between `1` and `99999`. A missing book returns `404 Not Found`.

#### `POST /books`

Creates and returns a new book:

```json
{
  "title": "Python Crash Course",
  "author": "Eric Matthes",
  "price": 39.99,
  "pages": 544,
  "year": 2019
}
```

The database generates the book ID.

#### `PATCH /books/{book_id}`

Updates and returns an existing book. Send only the fields that should
change:

```json
{
  "price": 34.99,
  "pages": 600
}
```

A missing book returns `404 Not Found`.

#### `DELETE /books/{book_id}`

Deletes a book:

```text
DELETE /books/1
```

A missing book returns `404 Not Found`.

## How the Database Session Works

`database.py` creates a SQLModel engine using `DATABASE_URL`.
`dependencies.py` provides a new SQLModel `Session` to each endpoint through
FastAPI's dependency injection. Create, update, and delete operations are
committed to SQLite, so their changes remain after the application restarts.

To start again with a new local database, stop the server, remove `store.db`,
and restart the application. The tables and initial example data will be
created again.

## Sample Data

On first run, the database is seeded with example data:

**Expenses:**
1. Bread: 1 KG for 3 NIS (2026-07-05)
2. Milk: 2 Litres for 5.5 NIS (2026-07-05)

**Books:**
1. Python by Eric Matthes (2019, 544 pages, $39.99)
2. Clean Code by Robert Martin (2008, 464 pages, $44.99)

## Learning Objectives

This project teaches:
- Building production-ready APIs with FastAPI
- Database integration with SQLModel
- Dependency injection patterns
- Request/response validation with Pydantic
- RESTful API design principles
- Environment-based configuration
- Error handling and HTTP status codes
- Type-safe Python development
- Implementing multiple CRUD APIs with consistent patterns
