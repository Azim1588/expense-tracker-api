# 01 — Create an expense

**Status:** ☐ Verify in your own repository  
**Contract:** `POST /expenses/` → `201 Created`  
**Files:** `main.py`, `schemas.py`, `models.py`, `database.py`

## 1. Requirement

**User story:** As a user, I want to record an expense so that I can track my spending.

**Problem solved:** Persist a validated expense beyond the lifetime of the FastAPI process. The client should not choose its database ID.

**Request JSON:**

```json
{
  "name": "Lunch",
  "amount": "12.50",
  "category": "Food",
  "date": "2026-11-21",
  "notes": "Client meeting"
}
```

`notes` is optional; other fields are required. Assume the notes-column migration was applied to the database FastAPI actually uses.

**Success:** HTTP `201` and response containing the same expense fields **plus a generated integer `id`**. Invalid inputs should normally give `422`.

## 2. Logic

```text
1. Receive POST /expenses/ with JSON.
2. FastAPI/Pydantic validate fields using ExpenseCreate.
3. FastAPI supplies a SQLAlchemy Session through Depends(get_db).
4. Convert the validated request into an Expense ORM object.
5. Add it to the Session; commit the transaction.
6. Refresh its database values (including generated ID).
7. Validate/serialize it as ExpenseResponse; return 201.
8. Close the request's Session through get_db cleanup.
```

| Component | What | Why / problem solved |
|---|---|---|
| FastAPI | Matches route, invokes handler, returns HTTP status | HTTP interface |
| `ExpenseCreate` (Pydantic) | Checks data types and rules | Bad request inputs |
| `Expense` (ORM) | Represents the table row | Python ↔ table mapping |
| Session | Tracks new object and commits | Transactional persistence |
| PostgreSQL | Enforces constraints and assigns ID | Durable records + reliable identity |
| `ExpenseResponse` | Defines public output, including ID | Stable response contract |

## 3. Code

This is the Session 2/3 reference pattern. **Compare it with your actual current endpoint.**

```python
@app.post("/expenses/", response_model=ExpenseResponse, status_code=201)
def create_expense(
    expense_create: ExpenseCreate,
    db: Session = Depends(get_db),
):
    new_expense = Expense(**expense_create.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense
```

**Why:** `model_dump()` converts validated request data into Python values; `**` provides them as constructor keyword arguments. `add()` schedules an insert; `commit()` flushes SQL and commits; `refresh()` reloads DB state. `response_model` tells FastAPI to validate and serialize the outgoing data. With `from_attributes=True`, Pydantic can read ORM attributes.

**Not needed:** A new migration for a Pydantic-only change. A migration is needed *only* if the physical table schema needs to change (e.g. adding `notes`).

## 4. Test

Open `http://127.0.0.1:8000/docs` → `POST /expenses/` → **Try it out**.

| Test | Action | Expected | Actual / pass |
|---|---|---|---|
| Valid expense | Submit sample JSON above | `201`; `id` generated; notes echoed | ☐ |
| Notes omitted | Send required four fields | `201`; notes = null (with current schema) | ☐ |
| Invalid amount | `"amount": "-5.00"` | `422` | ☐ |
| Invalid date | `"date": "2026-15-45"` | `422` | ☐ |
| Durable storage | Restart Uvicorn; GET expenses | Existing row remains | ☐ |
| Verify DB | `SELECT id, name, notes FROM expenses ORDER BY id DESC LIMIT 5;` | Row present | ☐ |

**Things to explain afterward:** Why the client does not supply `id`; why 201 (not 200); why `db.add()` alone is insufficient; how the ORM receives its generated ID.

**Limitations to revisit:** Handling database failures, duplicate submissions, and authorization are out of scope for this session.
