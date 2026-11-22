# Expense Tracker — implementation learning journal

This folder documents **how each feature was designed and implemented**. Every page follows the same repeatable workflow:

**Requirement → Logic → Code → Test**

The purpose is to learn to translate a business requirement into a verifiable backend implementation rather than memorizing syntax.

> **Status:** This is a reference starter kit based on the Backend Engineering 101 practice project, **not a snapshot of your actual repository**. Compare each example with your current code, mark features you have actually tested, and adjust line references and expected behavior before publishing.

## Feature documentation

| Feature | Documentation | Suggested verification |
|---|---|---|
| Create expense | [01 — POST /expenses/](01-create-expense.md) | POST returns 201 with a database-generated ID |
| List expenses | [02 — GET /expenses/](02-list-expenses.md) | Returns stored expenses or an empty array |
| Get by ID | [03 — GET /expenses/{expense_id}](03-get-expense-by-id.md) | 200 for existing record; 404 otherwise |
| Replace expense | [04 — PUT /expenses/{expense_id}](04-update-expense.md) | 200, same ID, updated fields |
| Delete expense | [05 — DELETE /expenses/{expense_id}](05-delete-expense.md) | 204, then GET returns 404 |
| Optional notes | [06 — Notes and Alembic migration](06-add-notes.md) | Verify real DB column and API response |
| Validation | [07 — Validation and error responses](07-validation-and-errors.md) | Invalid input returns 422 |
| Health check | [08 — GET /health](08-health-check.md) | 200 for live API process |
| Category filter (practice challenge) | [09 — Filtering by category](09-category-filter-challenge.md) | With filter, only matching expenses |

**Reusable resources:** [Template](TEMPLATE.md) · [Test matrix](TEST_MATRIX.md)

## How to document a new feature

1. Copy `TEMPLATE.md` to a named file (e.g. `10-expense-summary.md`).
2. Define success, failure, and edge-case behavior in **Requirement**.
3. Write **Logic** as numbered, plain-English pseudocode before coding.
4. Implement it in your application, then update **Code** with the relevant snippet and short explanation of *why* you used those components.
5. Run the exact requests in **Test**; record actual observed results. Do **not** mark a feature complete just because the sample code looks correct.
6. Commit implementation and documentation in the same feature branch when possible.

## Repository layout

```text
expense-tracker/
├── README.md                   # Project overview, setup, link to these docs
├── main.py                     # FastAPI route handlers (current learning version)
├── database.py                 # Engine, session factory, get_db
├── models.py                   # SQLAlchemy ORM models
├── schemas.py                  # Pydantic API contracts
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── versions/              # Actual migration history
└── docs/
    └── implementation/        # These feature journals
```

## Link from your root README

Add this line to your existing repository `README.md` without overwriting it:

```markdown
## Implementation practice
I document each feature as **Requirement → Logic → Code → Test** in the [implementation journal](docs/implementation/README.md).
```

**Security:** Never commit `.env`, database passwords, private keys, `.venv/`, or logs with credentials. Example test JSON may be committed if it contains only invented data.
