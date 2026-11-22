# 08 — Health check endpoint

**Status:** ☐ Verify in your own repository  
**Contract:** `GET /health` → `200 OK`

## 1. Requirement

A caller should have a lightweight way to tell that the FastAPI process is serving HTTP requests. **Problem solved:** Basic liveness signal for local testing and monitoring.

**Expected:** `200` and `{"status":"healthy"}` when the HTTP app is running.

## 2. Logic

```text
1. Receive GET /health.
2. Match route in FastAPI.
3. Return a static JSON response without database access.
```

## 3. Code

```python
@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

**Why:** Fast and simple. It does **not** check whether PostgreSQL is up, so it is a basic liveness check, **not** database readiness.

## 4. Test

| Case | Action | Expected | Verified? |
|---|---|---|---|
| App running | `GET /health` | 200 and healthy JSON | ☐ |
| DB stopped locally | Stop PostgreSQL test container; `GET /health` | May still return 200 (no DB dependency) | ☐ |
| DB stopped locally | `GET /expenses/` | Database operation fails; see logs | ☐ |

**Caution:** Only stop your own local practice container, not a shared or production database. Restart it afterward.

**Future improvement:** Define a separate `/ready` endpoint that verifies dependencies before a load balancer sends traffic.
