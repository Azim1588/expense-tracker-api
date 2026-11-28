from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class ExpenseBase(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=100
    )

    amount: Decimal = Field(
        gt=0,
        max_digits=12,
        decimal_places=2
    )

    category: str = Field(
        min_length=1,
        max_length=50
    )

    date: date


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(ExpenseBase):
    pass


class ExpenseResponse(ExpenseBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True
    )