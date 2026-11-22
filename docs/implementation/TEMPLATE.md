# [Feature name] — implementation journal

**Status:** ☐ Planned ☐ In progress ☐ Tested  
**HTTP contract:** `[METHOD] /route`  
**Code location:** `main.py` / `schemas.py` / `models.py` / `database.py` / `alembic/versions/...`  
**Prerequisites:** [database table / schema migration / endpoint]

## 1. Requirement — What must the system do?

**User story:** As a [type of user], I want [action], so that [benefit].

**Problem solved:** [Why this feature is needed.]

**Input:** [HTTP method, path, path/query/body fields, required vs optional.]

**Success:** [Status code, exact response shape, effect on database.]

**Failures and edge cases:** [Invalid input, missing record, empty results, duplicates, unavailable DB.]

**Acceptance criteria:**
- [ ] [Observable outcome #1]
- [ ] [Observable outcome #2]
- [ ] [Expected error condition]

## 2. Logic — How should it work? (before coding)

```text
1. Receive ...
2. Validate ...
3. Obtain database session ...
4. Perform database operation ...
5. Handle not-found / invalid condition ...
6. Commit if changing data ...
7. Return ...
```

**Components and why:**

| Component | What it does in this feature | Problem solved |
|---|---|---|
| FastAPI | ... | ... |
| Pydantic | ... | ... |
| SQLAlchemy Session | ... | ... |
| PostgreSQL | ... | ... |
| Alembic (if needed) | ... | ... |

## 3. Code — How did I implement it?

**Implementation:** Link to actual code in GitHub, or quote a *short* important excerpt. Keep source code in source files, not duplicated in full here.

```python
# Replace with your real implementation or a small excerpt
```

**Walkthrough:** Explain important lines in your own words.

**Design choices:** Why this method/SQLAlchemy method/status code? What did you choose *not* to implement?

**Schema or migration required?** [Yes/No, reason; reference revision if applicable.]

## 4. Test — What evidence proves it works?

**Environment:** local FastAPI + PostgreSQL; database: `[name]`; test with disposable data.

| Case | Request / action | Expected result | Actual result | Pass? |
|---|---|---|---|---|
| Happy path | ... | ... | [fill after test] | ☐ |
| Invalid input | ... | ... | [fill after test] | ☐ |
| Missing record | ... | ... | [fill after test] | ☐ |
| Persistence / DB verification | ... | ... | [fill after test] | ☐ |

**Swagger UI:** `http://127.0.0.1:8000/docs`

**Database verification (if applicable):** Open psql and run a read-only SELECT.

**Evidence:** [command output, screenshot of *non-sensitive* response, test run, git commit hash]

## 5. What I learned / next improvement

**I can now explain:** [the full request → DB → response flow]

**Limitations:** [e.g. no auth yet, no pagination yet]

**Next experiment:** [one modification to implement without copying]
