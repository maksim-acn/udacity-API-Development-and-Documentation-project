# Trivia API - Implementation Plan

## Overview
Complete the Trivia API Flask backend by implementing all TODO items: database setup, CORS, 7 REST endpoints, 4 error handlers, unit tests, and API documentation—per the Udacity course rubric.

> **Note**: This repo was forked from Udacity LMS and will be auto-graded. Follow the original design patterns exactly.

---

## Step 1: Database Setup

1. Create the development database:
   ```bash
   createdb trivia
   psql trivia < backend/trivia.psql
   ```
2. Create the test database:
   ```bash
   createdb trivia_test
   psql trivia_test < backend/trivia.psql
   ```

---

## Step 2: CORS Setup

**File**: `backend/flaskr/__init__.py`

- Initialize `CORS(app)`
- Add `@app.after_request` handler with headers:
  - `Access-Control-Allow-Headers`: `Content-Type,Authorization`
  - `Access-Control-Allow-Methods`: `GET,POST,DELETE,OPTIONS`

---

## Step 3: Implement API Endpoints

**File**: `backend/flaskr/__init__.py`

| # | Method | Endpoint | Purpose |
|---|--------|----------|---------|
| 1 | GET | `/categories` | Return all categories as `{id: type}` dict |
| 2 | GET | `/questions?page=N` | Paginated questions (10/page), include categories, total |
| 3 | DELETE | `/questions/<id>` | Delete question by ID |
| 4 | POST | `/questions` | Create new question (if no `searchTerm`) |
| 5 | POST | `/questions` | Search questions (if `searchTerm` in body) |
| 6 | GET | `/categories/<id>/questions` | Questions filtered by category |
| 7 | POST | `/quizzes` | Return random question not in `previous_questions` |

---

## Step 4: Implement Error Handlers

**File**: `backend/flaskr/__init__.py`

Implement `@app.errorhandler` for: **400, 404, 422, 500**

Response format:
```json
{
  "success": false,
  "error": 404,
  "message": "resource not found"
}
```

---

## Step 5: Write Unit Tests

**File**: `backend/test_flaskr.py`

- Use `unittest` library
- At least one **success test** per endpoint
- At least one **error test** per endpoint
- Use **create/cleanup** approach: tests create their own records and clean up after

| Endpoint | Success Test | Error Test |
|----------|--------------|------------|
| GET /categories | ✓ | ✓ |
| GET /questions | ✓ | ✓ (invalid page) |
| DELETE /questions/<id> | ✓ | ✓ (non-existent ID) |
| POST /questions (create) | ✓ | ✓ (missing fields) |
| POST /questions (search) | ✓ | ✓ |
| GET /categories/<id>/questions | ✓ | ✓ (invalid category) |
| POST /quizzes | ✓ | ✓ |

---

## Step 6: Document API in README

**File**: `backend/README.md`

Add detailed documentation for each endpoint:
- HTTP Method & URL
- Request parameters/body
- Response body example
- Error responses

---

## Rubric Checklist

- [ ] PEP 8 compliant code
- [ ] RESTful endpoint naming
- [ ] CORS enabled
- [ ] All 7 endpoints implemented
- [ ] All 4 error handlers implemented
- [ ] Unit tests for success + error per endpoint
- [ ] API documentation in README
- [ ] Secrets in environment variables (if any)
- [ ] `.gitignore` excludes virtualenv and local files
