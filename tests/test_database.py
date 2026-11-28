from sqlalchemy import text


# =====================================================
# 1. Verify Test Database Connection
# =====================================================

def test_database_connection(db_session):

    database_name = db_session.execute(
        text("SELECT current_database()")
    ).scalar_one()

    assert database_name == "expense_test_db"


# =====================================================
# 2. Verify Expenses Table Exists
# =====================================================

def test_expenses_table_exists(db_session):

    result = db_session.execute(
        text("SELECT to_regclass('public.expenses')")
    ).scalar_one()

    assert result == "expenses"


# =====================================================
# 3. Verify Database Cleanup
# =====================================================

def test_database_is_empty(clean_database, db_session):

    count = db_session.execute(
        text("SELECT COUNT(*) FROM expenses")
    ).scalar_one()

    assert count == 0