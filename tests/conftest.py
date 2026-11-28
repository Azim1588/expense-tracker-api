import os

import pytest

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

from main import app
from database import get_db


# =====================================================
# 1. Load Test Environment Configuration
# =====================================================

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise RuntimeError("TEST_DATABASE_URL is not configured")


# =====================================================
# 2. Protect Development Database
# =====================================================

test_url = make_url(TEST_DATABASE_URL)

if test_url.database != "expense_test_db":
    raise RuntimeError(
        "Tests must use the expense_test_db database"
    )


# =====================================================
# 3. Test Database Engine Fixture
# =====================================================

@pytest.fixture(scope="session")
def test_engine():

    engine = create_engine(
        TEST_DATABASE_URL,
        pool_pre_ping=True,
        hide_parameters=True,
        connect_args={"connect_timeout": 5}
    )

    try:

        # Verify the actual database connection
        with engine.connect() as connection:

            database_name = connection.execute(
                text("SELECT current_database()")
            ).scalar_one()

            if database_name != "expense_test_db":
                raise RuntimeError("Incorrect test database")

        yield engine

    finally:

        engine.dispose()


# =====================================================
# 4. Database Cleanup Fixture
# =====================================================

@pytest.fixture(scope="function")
def clean_database(test_engine):

    # Clean database before the test
    with test_engine.begin() as connection:

        connection.execute(
            text("TRUNCATE TABLE expenses RESTART IDENTITY")
        )

    try:

        yield

    finally:

        # Clean database after the test
        with test_engine.begin() as connection:

            connection.execute(
                text("TRUNCATE TABLE expenses RESTART IDENTITY")
            )


# =====================================================
# 5. Test Database Session Fixture
# =====================================================

@pytest.fixture(scope="function")
def db_session(test_engine, clean_database):

    TestingSessionLocal = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False
    )

    db = TestingSessionLocal()

    try:

        yield db

    finally:

        db.rollback()
        db.close()


# =====================================================
# 6. FastAPI Test Client Fixture
# =====================================================

@pytest.fixture(scope="function")
def client(test_engine, clean_database):

    # Create a session factory for test requests
    TestingSessionLocal = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False
    )

    # Define replacement database dependency
    def override_get_db():

        db = TestingSessionLocal()

        try:

            yield db

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()

    # Register dependency override
    app.dependency_overrides[get_db] = override_get_db

    try:

        # Create and provide the test client
        with TestClient(app) as test_client:

            yield test_client

    finally:

        # Remove dependency override
        app.dependency_overrides.pop(get_db, None)

# =====================================================
# 7. Sample Expense Fixture
# =====================================================

@pytest.fixture
def sample_expense():

    return {
        "name": "Groceries",
        "amount": "75.50",
        "category": "Food",
        "date": "2026-11-26"
    }