from django.shortcuts import render
from quiz.models import Quiz
from quiz import constants as QUIZ_CONSTANTS
# Create your views here.


def quiz_home(request):
    template_name = "quiz/quiz_home.html"
    context = {
        'page_title': "Quiz Home",
    }
    return render(request, template_name, context)


def create_quiz(request):
    template_name = "quiz/quiz_create.html"
    context = {
        'page_title': "New Quiz",
        'QUIZ_TYPES' : QUIZ_CONSTANTS.QUIZ_TYPES,
        'QUIZ_TYPE_TOURNAMENT': QUIZ_CONSTANTS.QUIZ_TYPE_TOURNAMENT,
        'DESCRIPTION_MAX_SIZE' : QUIZ_CONSTANTS.DESCRIPTION_MAX_SIZE
    }
    return render(request, template_name, context)



def update_quiz(request, quiz_uuid):
    template_name = "quiz/quiz_update.html"
    context = {
        'page_title': "Update Quiz",
        'QUIZ_TYPES' : QUIZ_CONSTANTS.QUIZ_TYPES,
        'DESCRIPTION_MAX_SIZE' : QUIZ_CONSTANTS.DESCRIPTION_MAX_SIZE
    }
    return render(request, template_name, context)


def delete_quiz(request, quiz_uuid):
    template_name = "quiz/quiz_delete.html"
    context = {
        'page_title': "Delete Quiz",
    }
    return render(request, template_name, context)


def create_question(request, quiz_uuid):
    template_name = "quiz/question_create.html"
    context = {
        'page_title': "New Question",
        'DESCRIPTION_MAX_SIZE' : QUIZ_CONSTANTS.DESCRIPTION_MAX_SIZE,
        'QUESTION_TYPE_MCQ' : QUIZ_CONSTANTS.QUESTION_TYPE_MCQ
    }
    return render(request, template_name, context)


def start_quiz(request, quiz_uuid):
    template_name = "quiz/quiz_start.html"
    context = {
        'page_title': "Start Quiz",
    }
    return render(request, template_name, context)


def stop_quiz(request, quiz_uuid):
    template_name = "quiz/quiz_stop.html"
    context = {
        'page_title': "Stop Quiz",
    }
    return render(request, template_name, context)


def quiz_detail(request, quiz_uuid):
    template_name = "quiz/quiz.html"
    context = {
        'page_title': "New Quiz",
    }
    return render(request, template_name, context)

def quiz_detail_slug(request, slug):
    template_name = "quiz/quiz.html"
    context = {
        'page_title': "Quiz",
    }
    return render(request, template_name, context)