import pytest

from decimal import Decimal
from sqlalchemy import select

from models import Expense


# =====================================================
# 1. CREATE EXPENSE
# =====================================================

def test_create_expense(client, sample_expense, db_session):

    response = client.post(
        "/expenses/",
        json=sample_expense
    )

    assert response.status_code == 201

    data = response.json()

    assert isinstance(data["id"], int)
    assert data["name"] == sample_expense["name"]
    assert Decimal(data["amount"]) == Decimal("75.50")
    assert data["category"] == sample_expense["category"]
    assert data["date"] == sample_expense["date"]

    # Verify PostgreSQL persistence
    expense = db_session.get(Expense, data["id"])

    assert expense is not None
    assert expense.name == sample_expense["name"]
    assert expense.amount == Decimal("75.50")


# =====================================================
# 2. READ EMPTY COLLECTION
# =====================================================

def test_get_empty_expenses(client):

    response = client.get("/expenses/")

    assert response.status_code == 200
    assert response.json() == []


# =====================================================
# 3. READ MULTIPLE EXPENSES
# =====================================================

def test_get_multiple_expenses(client, sample_expense):

    first = client.post(
        "/expenses/",
        json=sample_expense
    )

    second = client.post(
        "/expenses/",
        json={
            **sample_expense,
            "name": "Internet Bill"
        }
    )

    assert first.status_code == 201
    assert second.status_code == 201

    response = client.get("/expenses/")

    assert response.status_code == 200
    assert len(response.json()) == 2


# =====================================================
# 4. READ SINGLE EXPENSE
# =====================================================

def test_get_expense_by_id(client, sample_expense):

    created = client.post(
        "/expenses/",
        json=sample_expense
    )

    assert created.status_code == 201

    expense_id = created.json()["id"]

    response = client.get(f"/expenses/{expense_id}")

    assert response.status_code == 200
    assert response.json()["id"] == expense_id
    assert response.json()["name"] == sample_expense["name"]


# =====================================================
# 5. READ NONEXISTENT EXPENSE
# =====================================================

def test_get_expense_not_found(client):

    response = client.get("/expenses/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"


# =====================================================
# 6. UPDATE EXPENSE
# =====================================================

def test_update_expense(client, sample_expense, db_session):

    created = client.post(
        "/expenses/",
        json=sample_expense
    )

    assert created.status_code == 201

    expense_id = created.json()["id"]

    updated_payload = {
        "name": "Updated Groceries",
        "amount": "95.00",
        "category": "Shopping",
        "date": "2026-11-27"
    }

    response = client.put(
        f"/expenses/{expense_id}",
        json=updated_payload
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Groceries"
    assert Decimal(response.json()["amount"]) == Decimal("95.00")

    # Verify database update
    expense = db_session.get(Expense, expense_id)

    assert expense is not None
    assert expense.name == "Updated Groceries"
    assert expense.amount == Decimal("95.00")


# =====================================================
# 7. UPDATE NONEXISTENT EXPENSE
# =====================================================

def test_update_expense_not_found(client, sample_expense):

    response = client.put(
        "/expenses/999999",
        json=sample_expense
    )

    assert response.status_code == 404


# =====================================================
# 8. DELETE EXPENSE
# =====================================================

def test_delete_expense(client, sample_expense, db_session):

    created = client.post(
        "/expenses/",
        json=sample_expense
    )

    assert created.status_code == 201

    expense_id = created.json()["id"]

    response = client.delete(f"/expenses/{expense_id}")

    assert response.status_code == 204
    assert response.content == b""

    # Verify database deletion
    assert db_session.get(Expense, expense_id) is None

    # Verify resource is no longer accessible
    response = client.get(f"/expenses/{expense_id}")

    assert response.status_code == 404


# =====================================================
# 9. DELETE NONEXISTENT EXPENSE
# =====================================================

def test_delete_expense_not_found(client):

    response = client.delete("/expenses/999999")

    assert response.status_code == 404


# =====================================================
# 10. INVALID REQUEST DATA
# =====================================================

@pytest.mark.parametrize(
    "field, invalid_value",
    [
        ("amount", "-10.00"),
        ("amount", "0.00"),
        ("name", ""),
        ("date", "invalid-date"),
        ("amount", "10.123")
    ]
)
def test_invalid_expense(
    client,
    sample_expense,
    db_session,
    field,
    invalid_value
):

    sample_expense[field] = invalid_value

    response = client.post(
        "/expenses/",
        json=sample_expense
    )

    assert response.status_code == 422

    errors = response.json()["detail"]

    assert any(
        error["loc"][-1] == field
        for error in errors
    )

    # Verify invalid data was not persisted
    expenses = db_session.scalars(
        select(Expense)
    ).all()

    assert len(expenses) == 0


# =====================================================
# 11. MISSING REQUIRED FIELD
# =====================================================

def test_missing_required_field(
    client,
    sample_expense,
    db_session
):

    del sample_expense["name"]

    response = client.post(
        "/expenses/",
        json=sample_expense
    )

    assert response.status_code == 422

    assert db_session.scalars(
        select(Expense)
    ).all() == []


# =====================================================
# 12. INVALID UPDATE
# =====================================================

def test_invalid_update(client, sample_expense, db_session):

    created = client.post(
        "/expenses/",
        json=sample_expense
    )

    assert created.status_code == 201

    expense_id = created.json()["id"]

    response = client.put(
        f"/expenses/{expense_id}",
        json={
            **sample_expense,
            "amount": "-50.00"
        }
    )

    assert response.status_code == 422

    # Verify original record was not modified
    expense = db_session.get(Expense, expense_id)

    assert expense is not None
    assert expense.amount == Decimal("75.50")
    assert expense.name == sample_expense["name"]