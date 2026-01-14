# Trivia API - Copilot Instructions

## Project Overview
Full-stack trivia quiz app: Flask/SQLAlchemy REST API backend + React frontend. The backend API is **incomplete** and needs endpoint implementations in `backend/flaskr/__init__.py`.

## Architecture

### Backend (Flask + PostgreSQL)
- **Entry point**: `backend/flaskr/__init__.py` - Uses app factory pattern via `create_app()`
- **Models**: `backend/models.py` - `Question` and `Category` SQLAlchemy models with `format()` methods for JSON serialization
- **Database**: PostgreSQL with `trivia` (dev) and `trivia_test` (test) databases
- **Pagination**: 10 questions per page (constant `QUESTIONS_PER_PAGE`)

### Frontend (React)
- Proxies API requests to `http://127.0.0.1:5000/` (see `frontend/package.json`)
- Uses jQuery for AJAX calls to the backend
- Key components: `QuestionView.js`, `FormView.js`, `QuizView.js`

## Required API Endpoints

The frontend expects these exact endpoints and response formats:

| Endpoint | Method | Purpose | Response Keys |
|----------|--------|---------|---------------|
| `/categories` | GET | List all categories | `{ categories: { id: type } }` |
| `/questions?page=N` | GET | Paginated questions | `{ questions, total_questions, categories, current_category }` |
| `/questions/<id>` | DELETE | Delete a question | Status code only |
| `/questions` | POST | Create question OR search | Check for `searchTerm` in body to differentiate |
| `/categories/<id>/questions` | GET | Questions by category | `{ questions, total_questions, current_category }` |
| `/quizzes` | POST | Get next quiz question | `{ question }` - returns `null` when no more questions |

### POST `/questions` Dual Purpose
```python
# Differentiate by checking request body:
if 'searchTerm' in body:
    # Search: return matching questions
else:
    # Create: add new question with question, answer, difficulty, category
```

## Database Conventions

- **Categories format**: Return as `{ id: type_string }` dict, NOT array
- **Question.category**: Stored as string ID (e.g., "1"), not integer
- Models have `insert()`, `update()`, `delete()`, `format()` helper methods

## Error Handling Pattern
Implement error handlers returning JSON:
```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": 404, "message": "resource not found"}), 404
```
Required handlers: 400, 404, 422, 500

## Testing

Uses separate `trivia_test` database. Test file: `backend/test_flaskr.py`
```bash
# From backend/
dropdb trivia_test && createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
Each test method gets fresh tables via `setUp()`/`tearDown()`.

## Development Commands

```bash
# Backend (from backend/)
pip install -r requirements.txt
createdb trivia && psql trivia < trivia.psql
flask run --reload  # Runs on :5000

# Frontend (from frontend/)
npm install
npm start  # Runs on :3000, proxies to :5000
```

## Key Implementation Notes

1. **CORS**: Must enable with `CORS(app)` and set appropriate headers
2. **Quiz logic**: Track `previous_questions` IDs, return random question not in that list
3. **Search**: Case-insensitive substring match using `ilike('%term%')`
4. **Abort on errors**: Use Flask's `abort(404)`, `abort(422)` etc.
