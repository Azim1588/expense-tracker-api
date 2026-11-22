# 05 — Delete an expense

**Status:** ☐ Verify in your own repository  
**Contract:** `DELETE /expenses/{expense_id}` → `204 No Content`, or `404 Not Found`

## 1. Requirement

A user needs to remove an unwanted expense. **Problem solved:** Correct accidental entries or duplicates.

**Success:** A matching row is deleted and the API returns **204 with no response body**. Missing ID returns 404. The application should not delete other rows.

## 2. Logic

```text
1. Parse integer expense ID.
2. Obtain Session and query by primary key.
3. If absent, return 404.
4. Mark the ORM object for deletion.
5. Commit transaction.
6. Return no response body with status 204.
```

## 3. Code

```python
@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.get(Expense, expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
```

**Why:** `db.delete` marks the ORM object for deletion; `commit` flushes a DELETE and commits it. `204` is appropriate when no response body is returned.

## 4. Test

| Case | Action | Expected | Verified? |
|---|---|---|---|
| Existing disposable ID | DELETE | 204, empty body | ☐ |
| Read afterward | GET same ID | 404 | ☐ |
| Delete again | DELETE same ID again | 404 in this design | ☐ |
| Different record | GET another ID | Still present | ☐ |

**Future concern:** Hard deletion is irreversible without backups; some production systems use soft deletion. **Safety:** Only use a disposable test expense.
