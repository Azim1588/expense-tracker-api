import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# =====================================================
# 1. Load Environment Configuration
# =====================================================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured")


# =====================================================
# 2. Initialize SQLAlchemy Engine
# =====================================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    hide_parameters=True
)


# =====================================================
# 3. Configure Database Session Factory
# =====================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# =====================================================
# 4. Define SQLAlchemy Declarative Base
# =====================================================

class Base(DeclarativeBase):
    pass


# =====================================================
# 5. Database Session Dependency
# =====================================================

def get_db():

    # Create a database session
    db = SessionLocal()

    try:

        # Provide the session to the endpoint
        yield db

    except Exception:

        # Roll back any unsuccessful transaction
        db.rollback()

        # Propagate the original exception
        raise

    finally:

        # Release database session resources
        db.close()