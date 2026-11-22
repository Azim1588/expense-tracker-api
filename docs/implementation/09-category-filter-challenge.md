# 09 — Optional category filter (independent practice challenge)

**Status:** ☐ Planned ☐ Implemented ☐ Tested — **not assumed complete**  
**Contract:** `GET /expenses/?category=Food` → `200 OK`

## 1. Requirement

A user wants to see expenses in a specific category. If no `category` is supplied, preserve existing GET-all behavior. If the category has no matches, return `[]`. **Problem solved:** Targeted retrieval without downloading and filtering all rows on the client.

**Examples:**

- `GET /expenses/` → all expenses
- `GET /expenses/?category=Food` → Food expenses only
- `GET /expenses/?category=DoesNotExist` → `[]`

## 2. Logic — write this before coding

```text
1. Receive optional category query parameter.
2. Start with SELECT Expense ordered by id.
3. If category was supplied, add a WHERE condition.
4. Execute query through provided Session.
5. Return list of ExpenseResponse objects.
```

### Components and problems solved

| Component | Purpose |
|---|---|
| FastAPI query parameter | Parse optional category from URL |
| SQLAlchemy `select()` | Build query |
| `.where()` | Apply filtering at database layer |
| PostgreSQL | Retrieve only matching rows |
| Pydantic response | Consistent array response |

## 3. Code — implement yourself

**Hints, not a complete solution:**

```python
category: str | None = None       # optional query input
statement = select(Expense)       # start query
# statement = statement.where(Expense.category == category) when a category is supplied
```

No database migration is needed because the `category` column already exists. You typically don't need a new Pydantic body model for a simple query parameter.

**Your code link:** `[Add after implementation]`

## 4. Test

| Case | Action | Expected | Verified? |
|---|---|---|---|
| No filter | `GET /expenses/` | All rows | ☐ |
| Existing category | `GET /expenses/?category=Food` | Only Food rows | ☐ |
| Missing category | `GET /expenses/?category=NothingHere` | `[]` | ☐ |
| Persistence | Restart FastAPI; filter again | Same stored results | ☐ |

**Questions to answer:** Where should filtering happen—Python or SQL? Why does this use a query parameter instead of a new path? How would you test mixed-case category names?
