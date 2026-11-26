from datetime import date
from decimal import Decimal

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field


# =====================================================
# 1. Initialize FastAPI Application
# =====================================================

app = FastAPI(
    title="Expense Tracker API",
    description="Backend Engineering 101 Expense Tracker.",
    version="1.0.0",
)


# =====================================================
# 2. Define Pydantic Models
# =====================================================

# Request model: data provided by the client
class ExpenseCreate(BaseModel):
    name: str = Field(min_length=1)
    amount: Decimal = Field(gt=0)
    category: str = Field(min_length=1)
    date: date


# Response model: data returned by the server
class ExpenseResponse(ExpenseCreate):
    id: int


# =====================================================
# 3. Initialize In-Memory Storage
# =====================================================

expenses: list[ExpenseResponse] = []

# Counter for generating unique expense IDs
next_expense_id = 1


# =====================================================
# 4. CREATE — POST /expenses/
# =====================================================

@app.post(
    "/expenses/",
    response_model=ExpenseResponse,
    status_code=201
)
def create_expense(expense: ExpenseCreate):
    global next_expense_id

    # Create a new expense with a server-generated ID
    new_expense = ExpenseResponse(
        id=next_expense_id,
        **expense.model_dump()
    )

    # Increment ID for the next expense
    next_expense_id += 1

    # Store the expense
    expenses.append(new_expense)

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
def get_expenses():

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
def get_expense(expense_id: int):

    # Search for the expense by ID
    for expense in expenses:

        if expense.id == expense_id:
            return expense

    # Expense does not exist
    raise HTTPException(
        status_code=404,
        detail="Expense not found"
    )


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
    updated_data: ExpenseCreate
):

    # Search for the existing expense
    for index, expense in enumerate(expenses):

        if expense.id == expense_id:

            # Create updated expense while preserving ID
            updated_expense = ExpenseResponse(
                id=expense_id,
                **updated_data.model_dump()
            )

            # Replace the old expense
            expenses[index] = updated_expense

            # Return updated expense
            return updated_expense

    # Expense does not exist
    raise HTTPException(
        status_code=404,
        detail="Expense not found"
    )


# =====================================================
# 8. DELETE — DELETE /expenses/{expense_id}
# =====================================================

@app.delete(
    "/expenses/{expense_id}",
    status_code=204
)
def delete_expense(expense_id: int):

    # Search for the expense
    for index, expense in enumerate(expenses):

        if expense.id == expense_id:

            # Remove expense from storage
            expenses.pop(index)

            # Return HTTP 204 with no response body
            return Response(status_code=204)

    # Expense does not exist
    raise HTTPException(
        status_code=404,
        detail="Expense not found"
    )


# =====================================================
# 9. HEALTH CHECK — GET /health
# =====================================================

@app.get(
    "/health",
    status_code=200
)
def health_check():

    return {"status": "ok"}