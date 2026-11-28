from sqlalchemy import select

from models import Expense


# =====================================================
# 1. Verify API Connection
# =====================================================

def test_get_expenses(client):

    response = client.get("/expenses/")

    assert response.status_code == 200
    assert response.json() == []


# =====================================================
# 2. Verify API Writes to Test Database
# =====================================================

def test_create_expense_in_test_database(client, db_session):

    payload = {
        "name": "Integration Test Expense",
        "amount": "25.50",
        "category": "Testing",
        "date": "2026-11-26"
    }

    # Send HTTP request to FastAPI
    response = client.post(
        "/expenses/",
        json=payload
    )

    # Verify HTTP response
    assert response.status_code == 201

    response_data = response.json()

    # Verify response data
    assert response_data["name"] == payload["name"]

    # Query the test database independently
    statement = select(Expense).where(
        Expense.id == response_data["id"]
    )

    expense = db_session.scalars(statement).one()

    # Verify that the record exists in the test database
    assert expense.name == payload["name"]
    assert expense.category == payload["category"]


# =====================================================
# 3. Verify Test Isolation
# =====================================================

def test_database_is_clean_between_tests(client):

    response = client.get("/expenses/")

    assert response.status_code == 200
    assert response.json() == []