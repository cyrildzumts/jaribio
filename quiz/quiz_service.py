from django.forms import modelformset_factory
from django.forms import inlineformset_factory
from django.forms import ValidationError
from django.db import transaction
from quiz.models import Quiz, Question,QuizImage, QuizSession, QuizStep, Answer, Category
from quiz.forms import AnswerForm
from quiz import constants as QuizConstants
from core import core_tools
from jaribio import utils
import logging
import datetime

logger = logging.getLogger(__name__)


def create_quiz(data):
    quiz = core_tools.create_instance(Quiz, data)
    return quiz


def create_question(data):
    question = None
    try:
        with transaction.atomic():
            question = core_tools.create_instance(Question, data)
            answers = create_answers(question, data)
            logger.info("Question created")
    except Exception as e:
        logger.warn("Error on creating Question.")
        logger.exception(e)
    
    return question

def update_question(question, data):
    results = {}
    try:       
        with transaction.atomic():
            question = core_tools.update_instance(Question, question, data)
            answers = update_answers(question, data)
            results = {'question': question, 'answers': answers}
    except Exception as e:
        logger.error(f"Error on update question {question.question_uuid} : ")
        logger.exception(e)
    return results
    
def update_answers(question, data):
    AnswerFormset = inlineformset_factory(Question, Answer, fields=('content', 'is_correct'), extra=0, can_delete=False)
    formset = AnswerFormset(data, instance=question)
    try:
        if formset.is_valid():
            answers = formset.save()
            logger.info(f"Answers for question {question.question_uuid} updated")
            return answers
        else:
            logger.warn(f"Answers for question {question.question_uuid} not updated. Errors : {formset.errors}")
    except Exception as e:
        logger.warn(f"Answers for question {question.question_uuid} not updated. Error on validating or saving the formset")
        logger.exception(e)
        raise e

def create_answers(question, data):
    logger.info(f"quiz_service : creating answers for question {question}")
    Formset = modelformset_factory(Answer, form=AnswerForm)
    for i in range(4):
        data[f"form-{i}-question"] = question.pk
        data[f"form-{i}-created_by"] = question.created_by.pk
    formset = Formset(data)
    if formset.is_valid():
        answers = formset.save()
        logger.info("Saved Answer Formset")
        return answers
    else:
        msg = f"Answer Formset Error : {formset.errors} - Non form Errors : {formset.non_form_errors()}"
        logger.warn('Answer Formset is invalid')
        logger.error(f"Answer Formset Error : {msg}")
        raise ValidationError(msg)




def create_answer(data):
    answer = core_tools.create_instance(Answer, data)
    return answer

def create_quizstep(data):
    step = core_tools.create_instance(QuizStep, data)
    return step


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