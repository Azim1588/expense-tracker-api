from datetime import date
from decimal import Decimal

from sqlalchemy import (
    Integer,
    String,
    Numeric,
    Date,
    CheckConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Expense(Base):

    __tablename__ = "expenses"

    __table_args__ = (
        CheckConstraint(
            "amount > 0",
            name="ck_expenses_amount_positive"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )