from quiz.models import Quiz, Question,QuizImage, QuizSession, QuizStep, Answer, Category
from quiz import constants as QuizConstants
from core import core_tools
import logging
import datetime

logger = logging.getLogger(__name__)


def create_quiz(data):
    quiz = core_tools.create_instance(Quiz, data)
    return quiz


def create_question(data):
    pass

def create_answer(data):
    pass


def create_session(quiz, data):
    pass


def add_quiz_image(quiz, image):
    pass


def add_question_image(question, image):
    pass 

def create_category(data):
    pass


def start_quiz(quiz):
    pass


def stop_quiz(quiz):
    pass


def remove_session(quiz, session):
    pass


def update_session(session):
    pass


def answer_question(session, data):
    pass