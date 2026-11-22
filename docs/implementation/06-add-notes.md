# 06 — Add optional notes (schema + migration + API)

**Status:** ☐ Verify in your own repository  
**Change:** A new optional `notes` field, max 255 characters

## 1. Requirement

A user wants to attach context to an expense, such as “Client meeting.” Expenses without notes must remain valid, including existing database rows. **Problem solved:** Store optional free-text context without breaking old records.

**Expected API:** POST may include `"notes": "..."` or omit it; response contains notes or `null`. PUT can replace notes. Existing records have null notes until updated.

## 2. Logic

```text
1. Update ORM Expense model with nullable notes column.
2. Create/review Alembic migration to modify actual PostgreSQL table.
3. Apply migration to the same database FastAPI uses.
4. Update Pydantic ExpenseCreate schema (and response schema via inheritance).
5. Confirm create endpoint maps notes and update endpoint assigns notes.
6. Restart FastAPI; test Swagger and inspect PostgreSQL directly.
```

## 3. Code

**models.py (database mapping):**

```python
notes: Mapped[str | None] = mapped_column(String(255), nullable=True)
```

**schemas.py (API contract):**

```python
notes: str | None = Field(default=None, max_length=255, examples=["Client meeting"])
```

If `ExpenseResponse(ExpenseCreate)` and `model_config = ConfigDict(from_attributes=True)`, it inherits the new field. A POST endpoint using `Expense(**expense_create.model_dump())` includes notes without extra assignments. A PUT endpoint with manual assignments needs `expense.notes = expense_update.notes`.

**Migration workflow (only if not already migrated):**

```powershell
# Check which database this shell targets before invoking Alembic
$env:DATABASE_URL
python -m alembic current
python -m alembic revision --autogenerate -m "add notes to expenses"
# REVIEW the generated file, then:
python -m alembic upgrade head
```

**Important:** If the migration is already applied and only `schemas.py` changed, **do not generate another migration**. A Pydantic-only change does not alter the database table. `create_all()` does not upgrade existing tables either. If you migrated the practice DB but FastAPI uses the main DB, they have different schemas; check `DATABASE_URL`.

## 4. Test

| Case | Action | Expected | Verified? |
|---|---|---|---|
| Schema | `\d expenses` in psql | `notes` is `varchar(255)` nullable | ☐ |
| With notes | POST JSON including notes | 201, response contains text | ☐ |
| Omitted notes | POST JSON without notes | 201, notes null | ☐ |
| Long notes | Submit >255 chars | 422 | ☐ |
| Update notes | PUT existing ID with different notes | 200, updated text | ☐ |
| DB check | `SELECT id, notes FROM expenses ORDER BY id DESC LIMIT 5;` | Values match API | ☐ |

**Key lesson:** Database mapping, physical schema, API contract, and endpoint logic are different layers. Changes to one do not magically update the others.
