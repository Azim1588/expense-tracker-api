# 07 — Validation, constraints, and error responses

**Status:** ☐ Verify in your own repository

## 1. Requirement

The API should reject malformed expenses and clearly distinguish invalid inputs (`422`) from missing records (`404`). PostgreSQL should independently prevent nonpositive amounts. **Problem solved:** Prevent invalid data and give clients understandable feedback.

## 2. Logic

```text
1. Pydantic validates the JSON request before route handler logic.
2. If the request violates API constraints, FastAPI returns 422.
3. Otherwise the handler performs the operation.
4. For record lookup, return 404 if ID doesn't exist.
5. PostgreSQL independently enforces amount > 0 even for direct SQL writes.
6. On a failed database transaction, rollback the Session when continuing to use it.
```

## 3. Code

**schemas.py:**

```python
amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
name: str = Field(min_length=1, max_length=100)
category: str = Field(min_length=1, max_length=50)
date: datetime.date
notes: str | None = Field(default=None, max_length=255)
```

**models.py:**

```python
__table_args__ = (
    CheckConstraint("amount > 0", name="ck_expenses_amount_positive"),
)
```

**main.py (missing record):**

```python
if expense is None:
    raise HTTPException(status_code=404, detail="Expense not found")
```

**Why both Pydantic and PostgreSQL?** Pydantic improves feedback on HTTP input. The database constraint protects persisted data from writes through *any* client, including psql and other applications. A database constraint violation may produce an `IntegrityError`, which does not automatically become a 422 response unless your API catches/maps it.

## 4. Test

| Case | Request | Expected | Verified? |
|---|---|---|---|
| Positive amount | POST amount `"12.50"` | 201 | ☐ |
| Negative amount | POST amount `"-5.00"` | 422 | ☐ |
| Zero amount | POST amount `"0"` | 422 | ☐ |
| Invalid date | POST `"date": "hello"` | 422 | ☐ |
| Missing name | POST without name | 422 | ☐ |
| Nonexistent expense | GET high unused ID | 404 | ☐ |
| Database guard | Execute an INSERT with negative amount directly in psql | CHECK violation | ☐ |

**Important:** Test database constraint only on the database that actually has the constraint; migrations must have been applied. A failure within an open psql transaction must be rolled back before issuing subsequent commands.
