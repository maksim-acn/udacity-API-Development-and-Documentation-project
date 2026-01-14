from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    """Helper function to paginate questions."""
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    # Set up CORS. Allow '*' for origins.
    CORS(app, resources={r"/*": {"origins": "*"}})

    with app.app_context():
        db.create_all()

    @app.after_request
    def after_request(response):
        """Set Access-Control-Allow headers."""
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        """Handle GET requests for all available categories."""
        categories = Category.query.order_by(Category.id).all()
        
        if len(categories) == 0:
            abort(404)
        
        # Return categories as {id: type} dictionary
        categories_dict = {category.id: category.type for category in categories}
        
        return jsonify({
            'success': True,
            'categories': categories_dict
        })

    @app.route('/questions', methods=['GET'])
    def get_questions():
        """
        Handle GET requests for questions, including pagination.
        Returns list of questions, total questions, current category, categories.
        """
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        
        if len(current_questions) == 0:
            abort(404)
        
        # Get all categories as {id: type} dictionary
        categories = Category.query.order_by(Category.id).all()
        categories_dict = {category.id: category.type for category in categories}
        
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': categories_dict,
            'current_category': None
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """Delete a question using a question ID."""
        question = Question.query.filter(Question.id == question_id).one_or_none()
        
        if question is None:
            abort(404)
        
        try:
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except Exception:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_or_search_question():
        """
        POST endpoint to create a new question or search questions.
        If 'searchTerm' is in the request body, perform search.
        Otherwise, create a new question.
        """
        body = request.get_json()
        
        if body is None:
            abort(400)
        
        search_term = body.get('searchTerm', None)
        
        if search_term is not None:
            # Search for questions
            selection = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')
            ).order_by(Question.id).all()
            
            current_questions = paginate_questions(request, selection)
            
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'current_category': None
            })
        else:
            # Create a new question
            question = body.get('question', None)
            answer = body.get('answer', None)
            category = body.get('category', None)
            difficulty = body.get('difficulty', None)
            
            if not all([question, answer, category, difficulty]):
                abort(400)
            
            try:
                new_question = Question(
                    question=question,
                    answer=answer,
                    category=int(category),
                    difficulty=int(difficulty)
                )
                new_question.insert()
                
                return jsonify({
                    'success': True,
                    'created': new_question.id
                })
            except Exception:
                abort(422)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        """Get questions based on category."""
        category = Category.query.filter(Category.id == category_id).one_or_none()
        
        if category is None:
            abort(404)
        
        selection = Question.query.filter(
            Question.category == category_id
        ).order_by(Question.id).all()
        
        current_questions = paginate_questions(request, selection)
        
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'current_category': category.type
        })

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        """
        POST endpoint to get questions for quiz play.
        Takes category and previous question parameters.
        Returns a random question not in previous questions.
        """
        body = request.get_json()
        
        if body is None:
            abort(400)
        
        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)
        
        try:
            if quiz_category is None or quiz_category.get('id') == 0:
                # All categories
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)
                ).all()
            else:
                # Specific category
                category_id = quiz_category.get('id')
                questions = Question.query.filter(
                    Question.category == category_id,
                    Question.id.notin_(previous_questions)
                ).all()
            
            if len(questions) == 0:
                return jsonify({
                    'success': True,
                    'question': None
                })
            
            # Select a random question
            random_question = random.choice(questions)
            
            return jsonify({
                'success': True,
                'question': random_question.format()
            })
        except Exception:
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors."""
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors."""
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        """Handle 422 Unprocessable Entity errors."""
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 Internal Server Error."""
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    return app

