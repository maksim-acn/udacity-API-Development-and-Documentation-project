import os
import unittest

from flaskr import create_app
from models import db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_user = "postgres"
        self.database_password = "password"
        self.database_host = "localhost:5432"
        self.database_path = f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}/{self.database_name}"

        # Create app with the test configuration
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client()

    def tearDown(self):
        """Executed after each test"""
        pass

    # -------------------------------------------------------------------------
    # GET /categories Tests
    # -------------------------------------------------------------------------
    def test_get_categories_success(self):
        """Test GET /categories returns all categories."""
        res = self.client.get('/categories')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('categories', data)
        self.assertGreater(len(data['categories']), 0)

    # -------------------------------------------------------------------------
    # GET /questions Tests
    # -------------------------------------------------------------------------
    def test_get_questions_success(self):
        """Test GET /questions returns paginated questions."""
        res = self.client.get('/questions')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('questions', data)
        self.assertIn('total_questions', data)
        self.assertIn('categories', data)
        self.assertLessEqual(len(data['questions']), 10)

    def test_get_questions_with_page(self):
        """Test GET /questions with page parameter."""
        res = self.client.get('/questions?page=1')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertLessEqual(len(data['questions']), 10)

    def test_get_questions_invalid_page_404(self):
        """Test GET /questions with invalid page returns 404."""
        res = self.client.get('/questions?page=1000')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)

    # -------------------------------------------------------------------------
    # DELETE /questions/<id> Tests
    # -------------------------------------------------------------------------
    def test_delete_question_success(self):
        """Test DELETE /questions/<id> successfully deletes a question."""
        # First create a question to delete via API
        new_question = {
            'question': 'Test question to delete?',
            'answer': 'Test answer',
            'category': 1,
            'difficulty': 1
        }
        create_res = self.client.post('/questions', json=new_question)
        create_data = create_res.get_json()
        question_id = create_data['created']

        # Now delete it
        res = self.client.delete(f'/questions/{question_id}')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], question_id)

    def test_delete_question_not_found_404(self):
        """Test DELETE /questions/<id> with non-existent ID returns 404."""
        res = self.client.delete('/questions/99999')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)

    # -------------------------------------------------------------------------
    # POST /questions (Create) Tests
    # -------------------------------------------------------------------------
    def test_create_question_success(self):
        """Test POST /questions creates a new question."""
        new_question = {
            'question': 'What is 2 + 2?',
            'answer': '4',
            'category': 1,
            'difficulty': 1
        }
        res = self.client.post('/questions', json=new_question)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('created', data)
        
        # Clean up - delete the created question
        self.client.delete(f'/questions/{data["created"]}')

    def test_create_question_missing_fields_400(self):
        """Test POST /questions with missing fields returns 400."""
        incomplete_question = {
            'question': 'Incomplete question?'
            # Missing answer, category, difficulty
        }
        res = self.client.post('/questions', json=incomplete_question)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)

    # -------------------------------------------------------------------------
    # POST /questions (Search) Tests
    # -------------------------------------------------------------------------
    def test_search_questions_success(self):
        """Test POST /questions with searchTerm returns matching questions."""
        res = self.client.post('/questions', json={'searchTerm': 'title'})
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('questions', data)
        self.assertIn('total_questions', data)

    def test_search_questions_no_results(self):
        """Test POST /questions with searchTerm that has no matches."""
        res = self.client.post('/questions', json={'searchTerm': 'xyznonexistent123'})
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)

    def test_search_questions_case_insensitive(self):
        """Test POST /questions search is case-insensitive."""
        # Search with different cases - should return same results
        res_lower = self.client.post('/questions', json={'searchTerm': 'what'})
        res_upper = self.client.post('/questions', json={'searchTerm': 'WHAT'})
        
        data_lower = res_lower.get_json()
        data_upper = res_upper.get_json()

        self.assertEqual(res_lower.status_code, 200)
        self.assertEqual(res_upper.status_code, 200)
        self.assertEqual(data_lower['total_questions'], data_upper['total_questions'])

    # -------------------------------------------------------------------------
    # GET /categories/<id>/questions Tests
    # -------------------------------------------------------------------------
    def test_get_questions_by_category_success(self):
        """Test GET /categories/<id>/questions returns questions for category."""
        res = self.client.get('/categories/1/questions')  # Science
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('questions', data)
        self.assertIn('total_questions', data)
        self.assertIn('current_category', data)

    def test_get_questions_by_category_not_found_404(self):
        """Test GET /categories/<id>/questions with invalid category returns 404."""
        res = self.client.get('/categories/9999/questions')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)

    # -------------------------------------------------------------------------
    # POST /quizzes Tests
    # -------------------------------------------------------------------------
    def test_play_quiz_success(self):
        """Test POST /quizzes returns a random question."""
        quiz_data = {
            'previous_questions': [],
            'quiz_category': {'id': 0, 'type': 'click'}  # All categories
        }
        res = self.client.post('/quizzes', json=quiz_data)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('question', data)

    def test_play_quiz_specific_category(self):
        """Test POST /quizzes with specific category."""
        quiz_data = {
            'previous_questions': [],
            'quiz_category': {'id': 1, 'type': 'Science'}
        }
        res = self.client.post('/quizzes', json=quiz_data)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('question', data)

    def test_play_quiz_no_more_questions(self):
        """Test POST /quizzes returns null when all questions exhausted."""
        # First get all questions in a category
        cat_res = self.client.get('/categories/5/questions')  # Entertainment
        cat_data = cat_res.get_json()
        
        # Use all question IDs as previous_questions
        all_question_ids = [q['id'] for q in cat_data.get('questions', [])]
        
        # Make a large list of IDs that definitely includes all questions
        quiz_data = {
            'previous_questions': list(range(1, 100)),
            'quiz_category': {'id': 5, 'type': 'Entertainment'}
        }
        res = self.client.post('/quizzes', json=quiz_data)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        # When no questions available, question should be None
        self.assertIsNone(data['question'])

    # -------------------------------------------------------------------------
    # Error Handler Tests
    # -------------------------------------------------------------------------
    def test_404_error_handler(self):
        """Test 404 error handler returns proper JSON."""
        res = self.client.get('/nonexistent-endpoint')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_400_error_handler(self):
        """Test 400 error handler returns proper JSON."""
        # Send POST with empty JSON body (missing required fields)
        res = self.client.post('/questions', json={})
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
