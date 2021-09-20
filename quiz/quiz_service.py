from django.forms import modelformset_factory
from django.forms import inlineformset_factory
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
    question = core_tools.create_instance(Question, data)
    answers = create_answers(question, data)
    if answers:
        logger.info("Question created")
    else:
        logger.warn("Error on creating Question. Answers not valid. Rolling back")
        Question.objects.filter(pk=question.pk).delete()
        question = None
    return question

def update_question(question, data):
    question = core_tools.update_instance(Question, question, data)
    if question is None:
        return None
    answers = update_answers(question, data)
    return {'question': question, 'answers': answers}
    
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
        logger.warn(f"Answers for question {question.question_uuid} not updated. Error on validating the formset")
        logger.exception(e)
    return None

def create_answers(question, data):
    logger.info(f"quiz_service : creating answers for question {question}")
    Formset = modelformset_factory(Answer, form=AnswerForm)

    for i in range(4):
        data[f"form-{i}-question"] = question.pk
        data[f"form-{i}-created_by"] = question.created_by.pk
    formset = Formset(data)
    answers = None
    utils.show_dict_contents(data, "Forms Management")
    try:
        if formset.is_valid():
            answers = formset.save()
            logger.info("Saved Answer Formset")
        else:
            answers = None
            logger.warn('Answer Formset is invalid')
            logger.error(f"Answer Formset Error : {formset.errors}")
            logger.error(f"Answer Formset Non Form Error : {formset.non_form_errors()}")
    except Exception as e:
        logger.warn(f"Error on processing Answer Formset : ")
        logger.exception(e)
        logger.error(f"Answer Formset Error : {formset.errors}")
        logger.error(f"Answer Formset Non Form Error : {formset.non_form_errors()}")
    return answers



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