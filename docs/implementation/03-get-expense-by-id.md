# 03 — Retrieve one expense by ID

**Status:** ☐ Verify in your own repository  
**Contract:** `GET /expenses/{expense_id}` → `200 OK`, or `404 Not Found`

## 1. Requirement

A user needs to retrieve one specific expense using its stable database identifier. **Problem solved:** Identify a single row even if multiple expenses share the same name.

**Inputs:** `expense_id` is a required integer path parameter. No request body.

**Acceptance:** existing record → 200 with expense JSON; missing record → 404; non-integer ID → 422.

## 2. Logic

```text
1. Parse expense_id from the path as an integer.
2. Provide a database Session.
3. Retrieve Expense using its primary key.
4. If no row exists, raise 404.
5. Otherwise return ExpenseResponse with 200.
```

## 3. Code

```python
@app.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.get(Expense, expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense
```

**Why `db.get()`?** It is designed for primary-key lookup and may reuse an object already in the Session identity map. `None` means no matching record. `HTTPException` maps the missing resource to an HTTP 404 instead of raising an unrelated Python error.

## 4. Test

| Case | Input | Expected | Verified? |
|---|---|---|---|
| Existing ID | `/expenses/<real_id>` | 200, matching ID | ☐ |
| Missing ID | `/expenses/9999999` | 404 | ☐ |
| Noninteger ID | `/expenses/abc` | 422 | ☐ |
| Verify table | `SELECT * FROM expenses WHERE id = <real_id>;` | Same record | ☐ |

**Next experiment:** Decide whether a malformed ID should be handled by path validation or by querying the database.
