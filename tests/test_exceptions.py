import pytest

from sqlalchemy.orm import Session

from sqlalchemy.exc import (
    IntegrityError,
    OperationalError,
    TimeoutError,
    SQLAlchemyError
)


# =====================================================
# 1. DATABASE FAILURE RESPONSES
# =====================================================

@pytest.mark.parametrize(
    "exception, expected_status, expected_detail",
    [
        (
            IntegrityError(
                "TEST",
                {},
                Exception("Simulated integrity error")
            ),
            409,
            "Database integrity conflict"
        ),
        (
            OperationalError(
                "TEST",
                {},
                Exception("Simulated connection failure")
            ),
            503,
            "Database temporarily unavailable"
        ),
        (
            TimeoutError("Simulated timeout"),
            503,
            "Database temporarily unavailable"
        ),
        (
            SQLAlchemyError("Simulated database failure"),
            500,
            "Internal database error"
        )
    ]
)
def test_database_exception_handling(
    client,
    monkeypatch,
    exception,
    expected_status,
    expected_detail
):

    # Simulate a database failure
    def raise_database_error(*args, **kwargs):
        raise exception

    # Temporarily replace the SQLAlchemy query method
    monkeypatch.setattr(
        Session,
        "scalars",
        raise_database_error
    )

    # Execute the endpoint
    response = client.get("/expenses/")

    # Verify centralized exception handling
    assert response.status_code == expected_status

    assert response.json() == {
        "detail": expected_detail
    }


# =====================================================
# 2. APPLICATION HEALTH CHECK
# =====================================================

def test_health_check(client):

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}