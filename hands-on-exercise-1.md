# Hands-on Exercise 1: Build a Books API

In this exercise, you will use what you learned from the expenses API to build
a simple API for books.

Use the expenses code in `router/expenses.py` and `database.py` as a reference.
Try to write the books implementation yourself instead of copying every line.

## Your Task

Build an in-memory database and CRUD API for books.

### 1. Create an In-Memory Books Database

Add a Python list named `books` to `database.py`.

Add at least two example books to the list. Think about the information that is
useful for describing a book and choose suitable fields yourself.

Every book must have a unique `id`. You might also consider fields such as the
book's title, author, price, number of pages, or publication year. You do not
have to use all of these suggestions, and you may add other useful fields.

### 2. Create Three Pydantic Models

In `router/books.py`, create these three models:

- `BookCreate`: describes the request body used to create a book. The client
  should not provide the book's ID.
- `BookUpdate`: describes the request body used to update a book. Its fields
  should be optional so the client can update only the values that need to
  change.
- `BookPublic`: describes the book data that your API returns to the client.

The fields in these models should match the book fields you chose for your
in-memory database.

### 3. Implement CRUD Operations

Create the following endpoints in `router/books.py`:

| Method | Endpoint | What it should do |
| --- | --- | --- |
| `GET` | `/books` | Return all books. |
| `GET` | `/books/{book_id}` | Return one book using its ID. |
| `POST` | `/books` | Create and store a new book. |
| `PATCH` | `/books/{book_id}` | Update some fields of an existing book. |
| `DELETE` | `/books/{book_id}` | Delete a book using its ID. |

Your implementation should:

- Give every new book a unique ID.
- Return a `404 Not Found` error when a requested book does not exist.
- Use the appropriate Pydantic model for each request body.
- Use `BookPublic` as the response model where appropriate.
- Change the `books` list when a book is created, updated, or deleted.

### 4. Add the Books Router to the Application

Import the books router in `main.py` and include it in the FastAPI application.
Look at how the expenses and users routers are included for guidance.

When this step is complete, the books endpoints should appear in `/docs`.

## Extra Improvements

The following improvements are a plus:

- Add suitable `Field` validation to your Pydantic models. For example, think
  about which text fields should not be empty and which numbers must be
  positive.
- Add suitable `Path` validation for `book_id`.
- Add a useful `Query` parameter to `GET /books`, such as filtering by author,
  minimum price, or publication year.
- Use clear and meaningful names for variables, endpoint arguments, and
  Pydantic fields. For example, `book_id` is clearer than only `id`.

Choose validation rules that make sense for the book fields you created.

## Test Your Work

Run the application:

```cmd
uvicorn main:app --reload
```

Open the interactive documentation:

```text
http://127.0.0.1:8000/docs
```

Use the documentation to check that you can:

1. Get the initial list of books.
2. Get one book by its ID.
3. Create a new book.
4. Update the new book.
5. Delete the new book.
6. Receive a `404 Not Found` response when a book does not exist.

Remember that this is an in-memory database. Your changes will disappear when
the application restarts.

## Completion Checklist

- [ ] A `books` list exists in `database.py`.
- [ ] The list contains at least two example books.
- [ ] `BookCreate`, `BookUpdate`, and `BookPublic` are implemented.
- [ ] All five books endpoints work.
- [ ] Missing books return `404 Not Found`.
- [ ] The books router is included in `main.py`.
- [ ] The endpoints appear and work in `/docs`.
- [ ] Names are clear and validations make sense.
