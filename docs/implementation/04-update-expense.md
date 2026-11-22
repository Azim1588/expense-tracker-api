# 04 — Replace an expense (PUT)

**Status:** ☐ Verify in your own repository  
**Contract:** `PUT /expenses/{expense_id}` → `200 OK`, or `404 Not Found`

## 1. Requirement

A user entered incorrect information and wants to replace the editable fields while keeping the same expense ID. **Problem solved:** Fix existing records without creating duplicates.

**Inputs:** Existing integer ID plus complete `ExpenseCreate` request body. The current learning version treats PUT as a full replacement. `notes` is optional in the schema; omitting it sets the existing notes to `None`.

## 2. Logic

```text
1. Validate the ID and the replacement request body.
2. Get a database Session.
3. Retrieve the existing expense by ID.
4. If absent, return 404.
5. Assign updated fields to the tracked ORM object.
6. Commit changes; refresh and return the record.
```

## 3. Code

```python
@app.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense_update: ExpenseCreate,
    db: Session = Depends(get_db),
):
    expense = db.get(Expense, expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    expense.name = expense_update.name
    expense.amount = expense_update.amount
    expense.category = expense_update.category
    expense.date = expense_update.date
    expense.notes = expense_update.notes
    db.commit()
    db.refresh(expense)
    return expense
```

**Why:** SQLAlchemy tracks attribute changes; the Session flushes an UPDATE on commit. No new ORM object or new database ID is required. For partial field changes where omissions *should not* clear existing values, use a separate PATCH schema/endpoint later.

## 4. Test

Create a disposable expense and record its actual ID.

| Case | Action | Expected | Verified? |
|---|---|---|---|
| Update amount | PUT same ID with amount 15.50 and other required fields | 200, same ID, amount 15.50 | ☐ |
| Omit notes | PUT without notes | 200, notes null | ☐ |
| Missing record | PUT `/expenses/9999999` | 404 | ☐ |
| Invalid amount | PUT with `amount = -1` | 422 | ☐ |
| Persistence | GET updated record after API restart | New values remain | ☐ |

**Important:** Use a disposable row. Updating a real expense changes persistent data.
