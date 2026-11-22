# Expense Tracker — manual test matrix

Check off only after running these against your *current* local application. Always use test data and record the database URL target **without printing passwords**.

| Feature | Happy path | Failure / edge case | Database verification | Done? |
|---|---|---|---|---|
| POST create | 201, generated ID | 422 for negative amount | SELECT new record | ☐ |
| GET all | 200, array | Empty table -> [] | Compare SELECT | ☐ |
| GET by ID | 200, matching ID | 404 for missing ID | SELECT by ID | ☐ |
| PUT update | 200, same ID/new values | 404 if missing, 422 invalid | SELECT updated row | ☐ |
| DELETE | 204, no body | 404 on second delete | Row missing | ☐ |
| Notes | 201 with notes, 201 without | >255 chars -> 422 | `\d expenses` & SELECT notes | ☐ |
| Health | 200, healthy JSON | DB unavailable -> still may be 200 | No DB query by design | ☐ |
| Category filter (challenge) | 200, only matches | Unknown category -> [] | Compare WHERE query | ☐ |
| Persistence | Restart FastAPI | Existing records not lost | SELECT after restart | ☐ |
| Migration | `alembic upgrade head` | Don't reapply nonexistent revision | `\d expenses` | ☐ |

## Repeatable manual loop

1. Write down the requirement and expected status/JSON **before testing**.
2. Start Docker PostgreSQL and FastAPI; confirm both are using the *same intended database*.
3. Execute through Swagger UI (`/docs`).
4. Check HTTP status, JSON body, and Uvicorn logs.
5. Verify persisted changes using psql with SELECT.
6. Record **actual** observations in the corresponding feature journal.
7. Clean up only the disposable test rows you created.

## Useful psql commands

```sql
\dt
\d expenses
SELECT id, name, amount, category, notes FROM expenses ORDER BY id DESC LIMIT 10;
```

## What a passing test tells you

An HTTP status alone is not proof of persistence. A correct API result plus a database query (and, for writes, a restart check when relevant) gives stronger evidence that your layers work together.
