import pytest
import main

from fastapi.testclient import TestClient


# =====================================================
# 1. TEST CLIENT
# =====================================================

client = TestClient(main.app)


# =====================================================
# 2. TEST ISOLATION
# =====================================================

@pytest.fixture(autouse=True)
def reset_expenses():
    """
    Reset in-memory storage before and after each test.
    This ensures tests are independent.
    """

    # Setup
    main.expenses.clear()
    main.next_expense_id = 1

    yield

    # Cleanup
    main.expenses.clear()
    main.next_expense_id = 1


# =====================================================
# 3. REUSABLE TEST DATA
# =====================================================

def sample_expense():
    """
    Return valid expense data for testing.
    """

    return {
        "name": "Groceries",
        "amount": "85.50",
        "category": "Food",
        "date": "2026-11-23"
    }


# =====================================================
# TEST 1: CREATE EXPENSE
# POST /expenses/
# Expected: 201 Created
# =====================================================

def test_create_expense():

    # ARRANGE
    request_data = sample_expense()

    # ACT
    response = client.post(
        "/expenses/",
        json=request_data
    )

    # ASSERT
    assert response.status_code == 201

    response_data = response.json()

    assert response_data["id"] == 1
    assert response_data["name"] == "Groceries"
    assert response_data["amount"] == "85.50"
    assert response_data["category"] == "Food"
    assert response_data["date"] == "2026-11-23"

    # Verify expense was stored
    assert len(main.expenses) == 1


# =====================================================
# TEST 2: GET ALL EXPENSES
# GET /expenses/
# Expected: 200 OK
# =====================================================

def test_get_all_expenses():

    # ARRANGE
    client.post(
        "/expenses/",
        json=sample_expense()
    )

    # ACT
    response = client.get("/expenses/")

    # ASSERT
    assert response.status_code == 200

    response_data = response.json()

    assert isinstance(response_data, list)
    assert len(response_data) == 1
    assert response_data[0]["name"] == "Groceries"


# =====================================================
# TEST 3: GET EXPENSE BY ID
# GET /expenses/{expense_id}
# Expected: 200 OK
# =====================================================

def test_get_expense_by_id():

    # ARRANGE
    create_response = client.post(
        "/expenses/",
        json=sample_expense()
    )

    expense_id = create_response.json()["id"]

    # ACT
    response = client.get(
        f"/expenses/{expense_id}"
    )

    # ASSERT
    assert response.status_code == 200

    response_data = response.json()

    assert response_data["id"] == expense_id
    assert response_data["name"] == "Groceries"
    assert response_data["amount"] == "85.50"


# =====================================================
# TEST 4: UPDATE EXPENSE
# PUT /expenses/{expense_id}
# Expected: 200 OK
# =====================================================

def test_update_expense():

    # ARRANGE
    create_response = client.post(
        "/expenses/",
        json=sample_expense()
    )

    expense_id = create_response.json()["id"]

    updated_data = {
        "name": "Weekly Groceries",
        "amount": "120.75",
        "category": "Food",
        "date": "2026-11-23"
    }

    # ACT
    response = client.put(
        f"/expenses/{expense_id}",
        json=updated_data
    )

    # ASSERT
    assert response.status_code == 200

    response_data = response.json()

    assert response_data["id"] == expense_id
    assert response_data["name"] == "Weekly Groceries"
    assert response_data["amount"] == "120.75"

    # Verify updated data was stored
    get_response = client.get(
        f"/expenses/{expense_id}"
    )

    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Weekly Groceries"


# =====================================================
# TEST 5: DELETE EXPENSE
# DELETE /expenses/{expense_id}
# Expected: 204 No Content
# =====================================================

def test_delete_expense():

    # ARRANGE
    create_response = client.post(
        "/expenses/",
        json=sample_expense()
    )

    expense_id = create_response.json()["id"]

    # ACT
    response = client.delete(
        f"/expenses/{expense_id}"
    )

    # ASSERT
    assert response.status_code == 204
    assert response.content == b""

    # Verify expense was deleted
    get_response = client.get(
        f"/expenses/{expense_id}"
    )

    assert get_response.status_code == 404
    assert len(main.expenses) == 0


# =====================================================
# TEST 6: HEALTH CHECK
# GET /health
# Expected: 200 OK
# =====================================================

def test_health_check():

    # ACT
    response = client.get("/health")

    # ASSERT
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# =====================================================
# TEST 7: INVALID EXPENSE AMOUNT
# POST /expenses/
# Expected: 422 Validation Error
# =====================================================

def test_invalid_expense_amount():

    # ARRANGE
    invalid_data = sample_expense()

    invalid_data["amount"] = "-50.00"

    # ACT
    response = client.post(
        "/expenses/",
        json=invalid_data
    )

    # ASSERT
    assert response.status_code == 422

    # Verify invalid expense was not stored
    assert len(main.expenses) == 0


# =====================================================
# TEST 8: GET NONEXISTENT EXPENSE
# GET /expenses/{expense_id}
# Expected: 404 Not Found
# =====================================================

def test_get_nonexistent_expense():

    # ACT
    response = client.get("/expenses/999")

    # ASSERT
    assert response.status_code == 404

    assert response.json() == {
        "detail": "Expense not found"
    }


# =====================================================
# TEST 9: UPDATE NONEXISTENT EXPENSE
# PUT /expenses/{expense_id}
# Expected: 404 Not Found
# =====================================================

def test_update_nonexistent_expense():

    # ARRANGE
    updated_data = sample_expense()

    # ACT
    response = client.put(
        "/expenses/999",
        json=updated_data
    )

    # ASSERT
    assert response.status_code == 404

    assert response.json() == {
        "detail": "Expense not found"
    }


# =====================================================
# TEST 10: DELETE NONEXISTENT EXPENSE
# DELETE /expenses/{expense_id}
# Expected: 404 Not Found
# =====================================================

def test_delete_nonexistent_expense():

    # ACT
    response = client.delete("/expenses/999")

    # ASSERT
    assert response.status_code == 404

    assert response.json() == {
        "detail": "Expense not found"
    }