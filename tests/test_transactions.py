import pytest

from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from models import Expense


# =====================================================
# 1. DATABASE CHECK CONSTRAINT
# =====================================================

def test_database_rejects_negative_amount(db_session):

    expense = Expense(
        name="Invalid Expense",
        amount=Decimal("-10.00"),
        category="Testing",
        date=date.today()
    )

    db_session.add(expense)

    # PostgreSQL must reject the invalid amount
    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()

    # Verify nothing was persisted
    expenses = db_session.scalars(
        select(Expense)
    ).all()

    assert len(expenses) == 0


# =====================================================
# 2. TRANSACTION ATOMICITY
# =====================================================

def test_transaction_rollback(db_session):

    valid_expense = Expense(
        name="Valid Expense",
        amount=Decimal("25.00"),
        category="Testing",
        date=date.today()
    )

    invalid_expense = Expense(
        name="Invalid Expense",
        amount=Decimal("-10.00"),
        category="Testing",
        date=date.today()
    )

    # Insert the valid expense without committing
    db_session.add(valid_expense)
    db_session.flush()

    # Add an invalid expense to the same transaction
    db_session.add(invalid_expense)

    # The transaction must fail
    with pytest.raises(IntegrityError):
        db_session.commit()

    # Roll back the entire transaction
    db_session.rollback()

    expenses = db_session.scalars(
        select(Expense)
    ).all()

    # Neither record should exist
    assert len(expenses) == 0


# =====================================================
# 3. SESSION RECOVERY AFTER ROLLBACK
# =====================================================

def test_session_recovers_after_rollback(db_session):

    invalid_expense = Expense(
        name="Invalid Expense",
        amount=Decimal("-5.00"),
        category="Testing",
        date=date.today()
    )

    db_session.add(invalid_expense)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()

    # Reuse the session after rollback
    valid_expense = Expense(
        name="Recovery Expense",
        amount=Decimal("50.00"),
        category="Testing",
        date=date.today()
    )

    db_session.add(valid_expense)
    db_session.commit()
    db_session.refresh(valid_expense)

    assert valid_expense.id is not None

    expenses = db_session.scalars(
        select(Expense)
    ).all()

    assert len(expenses) == 1
    assert expenses[0].name == "Recovery Expense"