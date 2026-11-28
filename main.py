from fastapi import FastAPI, HTTPException, Response, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Expense
from schemas import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from exceptions import register_exception_handlers


# =====================================================
# 1. Initialize FastAPI Application
# =====================================================

app = FastAPI(
    title="Expense Tracker API",
    description="Backend Engineering 101 Expense Tracker.",
    version="1.0.0",
)

# Register centralized database exception handlers
register_exception_handlers(app)


# =====================================================
# 2. Pydantic Models
# =====================================================

# Request and response models are imported from schemas.py.
#
# ExpenseCreate   — Validates incoming expense data.
# ExpenseUpdate   — Validates expense update data.
# ExpenseResponse — Defines the API response structure.


# =====================================================
# 3. Database Storage and Session Management
# =====================================================

# PostgreSQL replaces the previous in-memory list.
#
# Expense — SQLAlchemy ORM model defined in models.py.
# get_db  — Database session dependency from database.py.
# Session — Manages database operations and transactions.
#
# PostgreSQL automatically generates unique expense IDs.
# FastAPI provides a database session for each CRUD request.
#
# Failed transactions are rolled back in database.py.
# Database exceptions are handled in exceptions.py.
# Database sessions are closed after each request.


# =====================================================
# 4. CREATE — POST /expenses/
# =====================================================

@app.post(
    "/expenses/",
    response_model=ExpenseResponse,
    status_code=201
)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db)
):

    # Convert validated Pydantic data into a SQLAlchemy object
    new_expense = Expense(
        **expense.model_dump()
    )

    # Register the new expense with the database session
    db.add(new_expense)

    # Execute pending changes and commit the transaction
    db.commit()

    # Reload the expense with database-generated values
    db.refresh(new_expense)

    # Return the created expense
    return new_expense


# =====================================================
# 5. READ ALL — GET /expenses/
# =====================================================

@app.get(
    "/expenses/",
    response_model=list[ExpenseResponse],
    status_code=200
)
def get_expenses(
    db: Session = Depends(get_db)
):

    # Construct a SELECT statement ordered by expense ID
    statement = select(Expense).order_by(Expense.id)

    # Execute the query and retrieve all expense objects
    expenses = db.scalars(statement).all()

    # Return all stored expenses
    return expenses


# =====================================================
# 6. READ ONE — GET /expenses/{expense_id}
# =====================================================

@app.get(
    "/expenses/{expense_id}",
    response_model=ExpenseResponse,
    status_code=200
)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db)
):

    # Retrieve the expense using its primary key
    expense = db.get(Expense, expense_id)

    # Expense does not exist
    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    # Return the requested expense
    return expense


# =====================================================
# 7. UPDATE — PUT /expenses/{expense_id}
# =====================================================

@app.put(
    "/expenses/{expense_id}",
    response_model=ExpenseResponse,
    status_code=200
)
def update_expense(
    expense_id: int,
    updated_data: ExpenseUpdate,
    db: Session = Depends(get_db)
):

    # Retrieve the existing expense using its primary key
    expense = db.get(Expense, expense_id)

    # Expense does not exist
    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    # Update expense attributes while preserving its ID
    expense.name = updated_data.name
    expense.amount = updated_data.amount
    expense.category = updated_data.category
    expense.date = updated_data.date

    # Persist the updated expense in PostgreSQL
    db.commit()

    # Reload the updated expense from the database
    db.refresh(expense)

    # Return the updated expense
    return expense


# =====================================================
# 8. DELETE — DELETE /expenses/{expense_id}
# =====================================================

@app.delete(
    "/expenses/{expense_id}",
    status_code=204
)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db)
):

    # Retrieve the expense using its primary key
    expense = db.get(Expense, expense_id)

    # Expense does not exist
    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    # Mark the expense for deletion
    db.delete(expense)

    # Commit the deletion to PostgreSQL
    db.commit()

    # Return HTTP 204 with no response body
    return Response(status_code=204)


# =====================================================
# 9. HEALTH CHECK — GET /health
# =====================================================

@app.get(
    "/health",
    status_code=200
)
def health_check():

    # Verify that the FastAPI application is running
    return {"status": "ok"}