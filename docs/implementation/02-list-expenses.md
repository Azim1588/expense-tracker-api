# 02 — List expenses

**Status:** ☐ Verify in your own repository  
**Contract:** `GET /expenses/` → `200 OK`

## 1. Requirement

A user needs to see previously recorded expenses. **Problem solved:** Read persisted records rather than an in-memory Python list. Return an empty JSON array (`[]`) if no rows exist. For learning, order by ID for predictable results; pagination can be added later.

## 2. Logic

```text
1. Receive GET /expenses/.
2. Obtain a SQLAlchemy Session.
3. Build SELECT for all Expense rows ordered by ID.
4. Execute and collect ORM objects.
5. Serialize as list[ExpenseResponse].
6. Return 200 with JSON array.
```

| Component | Role | Problem solved |
|---|---|---|
| FastAPI route | Exposes GET | Client retrieval interface |
| SQLAlchemy `select` | Describes query | No hand-written string SQL needed |
| Session `scalars().all()` | Executes and fetches Expense objects | Read data |
| Pydantic response model | Serializes every item | Consistent JSON |

## 3. Code

```python
@app.get("/expenses/", response_model=list[ExpenseResponse])
def get_expenses(db: Session = Depends(get_db)):
    statement = select(Expense).order_by(Expense.id)
    return db.scalars(statement).all()
```

`select(Expense)` describes a query; `db.scalars(statement).all()` fetches ORM objects. No commit is needed because no write is performed.

## 4. Test

| Case | Request | Expected | Verified? |
|---|---|---|---|
| Has rows | `GET /expenses/` | `200`, array with expenses | ☐ |
| Empty DB | `GET /expenses/` on empty practice DB | `200`, `[]` | ☐ |
| Restart API | Restart Uvicorn and GET again | Same persisted rows | ☐ |
| DB comparison | `SELECT * FROM expenses ORDER BY id;` | Corresponding records | ☐ |

**Design note:** Don't expose unbounded lists in a large production API; add pagination later. **Next experiment:** Implement `?category=Food` as an optional query filter (see feature 09).
