# Trivia API - Development Log

## Progress Tracker

| Step | Task | Status | Date | Notes |
|------|------|--------|------|-------|
| 1 | Database Setup | ✅ DONE | Jan 14, 2026 | Created trivia & trivia_test DBs, seeded with trivia.psql |
| 2 | CORS Setup | ✅ DONE | Jan 14, 2026 | CORS(app) + after_request headers |
| 3.1 | GET /categories | ✅ DONE | Jan 14, 2026 | Returns {id: type} dict |
| 3.2 | GET /questions | ✅ DONE | Jan 14, 2026 | Pagination with 10/page |
| 3.3 | DELETE /questions/<id> | ✅ DONE | Jan 14, 2026 | Returns deleted ID |
| 3.4 | POST /questions (create) | ✅ DONE | Jan 14, 2026 | Creates new question |
| 3.5 | POST /questions (search) | ✅ DONE | Jan 14, 2026 | Case-insensitive ilike search |
| 3.6 | GET /categories/<id>/questions | ✅ DONE | Jan 14, 2026 | Filter by category |
| 3.7 | POST /quizzes | ✅ DONE | Jan 14, 2026 | Random question not in previous |
| 4 | Error Handlers (400,404,422,500) | ✅ DONE | Jan 14, 2026 | JSON error responses |
| 5 | Unit Tests | ✅ DONE | Jan 14, 2026 | 18 tests passing |
| 6 | API Documentation | ✅ DONE | Jan 14, 2026 | Full docs in backend/README.md |

**Legend**: ⬜ TODO | 🔄 IN PROGRESS | ✅ DONE | ❌ BLOCKED

---

## Session Log

### Session 1 - January 14, 2026
- [x] Database setup (PostgreSQL, trivia & trivia_test databases)
- [x] CORS setup with after_request headers
- [x] Implemented all 7 endpoints
- [x] Implemented 4 error handlers (400, 404, 422, 500)
- [x] Wrote 18 unit tests (all passing)
- [x] Updated API documentation in README.md

**Key Fix**: Model had `category` as String but database uses Integer. Updated model and endpoints to use Integer for category field.

---

## Commands Reference

```bash
# Start backend (from backend/)
flask run --reload

# Start frontend (from frontend/)
npm start

# Run tests (from backend/)
python test_flaskr.py

# Reset test database (if needed)
PGPASSWORD=password psql -h localhost -U postgres -d trivia_test -f trivia.psql
```

---

## Issues & Resolutions

| Issue | Resolution | Date |
|-------|------------|------|
| `sudo -u postgres` fails | Use `sudo su postgres -c "..."` instead | Jan 14, 2026 |
| Category type mismatch (String vs Integer) | Updated model to use Integer, matching DB schema | Jan 14, 2026 |
| Test seeding failed due to type mismatch | Removed custom seeding, use pre-seeded trivia.psql data | Jan 14, 2026 |
| | | |
