# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Configure Environment Variables

Copy the environment template file and configure your database credentials:

```bash
cp .env.template .env
```

Edit `.env` with your database settings:

```env
DB_NAME=trivia
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost:5432
```

> **Note**: The `.env` file is ignored by git to keep your credentials secure.

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
FLASK_APP=flaskr flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

---

## API Reference

### Base URL

The API runs locally at `http://127.0.0.1:5000/`. This is set as a proxy in the frontend configuration.

### Error Handling

Errors are returned as JSON objects in the following format:

```json
{
    "success": false,
    "error": 404,
    "message": "resource not found"
}
```

The API returns the following error types:
- `400`: Bad Request
- `404`: Resource Not Found
- `422`: Unprocessable Entity
- `500`: Internal Server Error

---

### Endpoints

#### GET `/categories`

Fetches all available categories.

- **Request Arguments:** None
- **Returns:** An object with `success` and `categories` keys. Categories is a dictionary of `id: category_string` pairs.

**Example Request:**
```bash
curl http://127.0.0.1:5000/categories
```

**Example Response:**
```json
{
    "success": true,
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    }
}
```

---

#### GET `/questions`

Fetches a paginated list of questions (10 per page).

- **Request Arguments:**
  - `page` (optional, integer): Page number (default: 1)
- **Returns:** A list of questions, total number of questions, all categories, and current category.

**Example Request:**
```bash
curl http://127.0.0.1:5000/questions?page=1
```

**Example Response:**
```json
{
    "success": true,
    "questions": [
        {
            "id": 1,
            "question": "What is the capital of France?",
            "answer": "Paris",
            "category": 3,
            "difficulty": 1
        }
    ],
    "total_questions": 19,
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null
}
```

---

#### DELETE `/questions/<question_id>`

Deletes a question by ID.

- **Request Arguments:**
  - `question_id` (required, integer): The ID of the question to delete
- **Returns:** The ID of the deleted question.

**Example Request:**
```bash
curl -X DELETE http://127.0.0.1:5000/questions/5
```

**Example Response:**
```json
{
    "success": true,
    "deleted": 5
}
```

**Error Response (404):**
```json
{
    "success": false,
    "error": 404,
    "message": "resource not found"
}
```

---

#### POST `/questions`

Creates a new question OR searches for questions based on a search term.

##### Create a New Question

- **Request Body:**
  - `question` (required, string): The question text
  - `answer` (required, string): The answer text
  - `category` (required, integer): Category ID
  - `difficulty` (required, integer): Difficulty level (1-5)
- **Returns:** The ID of the created question.

**Example Request:**
```bash
curl -X POST http://127.0.0.1:5000/questions \
  -H "Content-Type: application/json" \
  -d '{"question":"What is 2+2?", "answer":"4", "category":1, "difficulty":1}'
```

**Example Response:**
```json
{
    "success": true,
    "created": 24
}
```

##### Search Questions

- **Request Body:**
  - `searchTerm` (required, string): The search term (case-insensitive)
- **Returns:** Questions matching the search term.

**Example Request:**
```bash
curl -X POST http://127.0.0.1:5000/questions \
  -H "Content-Type: application/json" \
  -d '{"searchTerm":"title"}'
```

**Example Response:**
```json
{
    "success": true,
    "questions": [
        {
            "id": 5,
            "question": "Whose longest novel has the title?",
            "answer": "Tom Jones",
            "category": 4,
            "difficulty": 4
        }
    ],
    "total_questions": 1,
    "current_category": null
}
```

---

#### GET `/categories/<category_id>/questions`

Fetches questions for a specific category.

- **Request Arguments:**
  - `category_id` (required, integer): The category ID
- **Returns:** Questions in the specified category.

**Example Request:**
```bash
curl http://127.0.0.1:5000/categories/1/questions
```

**Example Response:**
```json
{
    "success": true,
    "questions": [
        {
            "id": 20,
            "question": "What is the heaviest organ in the human body?",
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4
        }
    ],
    "total_questions": 3,
    "current_category": "Science"
}
```

**Error Response (404):**
```json
{
    "success": false,
    "error": 404,
    "message": "resource not found"
}
```

---

#### POST `/quizzes`

Gets a random question for quiz play, excluding previously asked questions.

- **Request Body:**
  - `previous_questions` (required, array): List of previously asked question IDs
  - `quiz_category` (required, object): Category object with `id` and `type` keys. Use `id: 0` for all categories.
- **Returns:** A random question not in `previous_questions`, or `null` if no questions remain.

**Example Request:**
```bash
curl -X POST http://127.0.0.1:5000/quizzes \
  -H "Content-Type: application/json" \
  -d '{"previous_questions":[1,2], "quiz_category":{"id":1, "type":"Science"}}'
```

**Example Response:**
```json
{
    "success": true,
    "question": {
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?",
        "answer": "Blood",
        "category": 1,
        "difficulty": 4
    }
}
```

**Response when no more questions:**
```json
{
    "success": true,
    "question": null
}
```

---

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
