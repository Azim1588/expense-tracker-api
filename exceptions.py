import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from sqlalchemy.exc import (
    IntegrityError,
    OperationalError,
    SQLAlchemyError,
    TimeoutError
)


# =====================================================
# 1. Initialize Application Logger
# =====================================================

logger = logging.getLogger(__name__)


# =====================================================
# 2. Register Database Exception Handlers
# =====================================================

def register_exception_handlers(app: FastAPI):

    # Handle database integrity violations
    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(
        request: Request,
        exc: IntegrityError
    ):
        logger.warning("Database integrity violation")

        return JSONResponse(
            status_code=409,
            content={"detail": "Database integrity conflict"}
        )

    # Handle database operational failures
    @app.exception_handler(OperationalError)
    async def operational_error_handler(
        request: Request,
        exc: OperationalError
    ):
        logger.error("Database operational failure")

        return JSONResponse(
            status_code=503,
            content={"detail": "Database temporarily unavailable"}
        )

    # Handle database resource timeouts
    @app.exception_handler(TimeoutError)
    async def timeout_error_handler(
        request: Request,
        exc: TimeoutError
    ):
        logger.error("Database resource timeout")

        return JSONResponse(
            status_code=503,
            content={"detail": "Database temporarily unavailable"}
        )

    # Handle unexpected SQLAlchemy failures
    @app.exception_handler(SQLAlchemyError)
    async def database_error_handler(
        request: Request,
        exc: SQLAlchemyError
    ):
        logger.error(
            "Unexpected database failure: %s",
            type(exc).__name__
        )

        return JSONResponse(
            status_code=500,
            content={"detail": "Internal database error"}
        )