from django.shortcuts import get_object_or_404, render
from quiz.models import Quiz
from quiz import constants as QUIZ_CONSTANTS
# Create your views here.


def quiz_home(request):
    template_name = "quiz/quiz_home.html"
    context = {
        'page_title': "Quiz Home",
        'quizzes': Quiz.objects.all()
    }
    return render(request, template_name, context)


def create_quiz(request):
    template_name = "quiz/quiz_create.html"
    context = {
        'page_title': "New Quiz",
        'QUIZ_TYPES' : QUIZ_CONSTANTS.QUIZ_TYPES,
        'QUIZ_TYPE_TOURNAMENT': QUIZ_CONSTANTS.QUIZ_TYPE_TOURNAMENT,
        'QUESTION_TYPES': QUIZ_CONSTANTS.QUESTION_TYPES,
        'QUESTION_TYPE_MCQ' : QUIZ_CONSTANTS.QUESTION_TYPE_MCQ,
        'DESCRIPTION_MAX_SIZE' : QUIZ_CONSTANTS.DESCRIPTION_MAX_SIZE,
    }
    return render(request, template_name, context)



def update_quiz(request, quiz_uuid):
    template_name = "quiz/quiz_update.html"
    quiz = get_object_or_404(Quiz, quiz_uuid=quiz_uuid)
    context = {
        'page_title': "Update Quiz",
        'quiz': quiz,
        'QUIZ_TYPES' : QUIZ_CONSTANTS.QUIZ_TYPES,
        'DESCRIPTION_MAX_SIZE' : QUIZ_CONSTANTS.DESCRIPTION_MAX_SIZE
    }
    return render(request, template_name, context)


def delete_quiz(request, quiz_uuid):
    template_name = "quiz/quiz_delete.html"
    quiz = get_object_or_404(Quiz, quiz_uuid=quiz_uuid)
    context = {
        'page_title': "Delete Quiz",
    }
    return render(request, template_name, context)


def create_question(request, quiz_uuid):
    template_name = "quiz/question_create.html"
    quiz = get_object_or_404(Quiz, quiz_uuid=quiz_uuid)
    context = {
        'page_title': "New Question",
        'quiz': quiz,
        'QUESTION_TYPES': QUIZ_CONSTANTS.QUESTION_TYPES,
        'DESCRIPTION_MAX_SIZE' : QUIZ_CONSTANTS.DESCRIPTION_MAX_SIZE,
        'QUESTION_TYPE_MCQ' : QUIZ_CONSTANTS.QUESTION_TYPE_MCQ
    }
    return render(request, template_name, context)


def create_quizstep(request, quiz_uuid):
    template_name = "quiz/question_create.html"
    quiz = get_object_or_404(Quiz, quiz_uuid=quiz_uuid)
    context = {
        'page_title': "New QuizStep",
        'quiz': quiz,
        'QUESTION_TYPES': QUIZ_CONSTANTS.QUESTION_TYPES,
        'DESCRIPTION_MAX_SIZE' : QUIZ_CONSTANTS.DESCRIPTION_MAX_SIZE,
        'QUESTION_TYPE_MCQ' : QUIZ_CONSTANTS.QUESTION_TYPE_MCQ
    }
    return render(request, template_name, context)


def start_quiz(request, quiz_uuid):
    template_name = "quiz/quiz_start.html"
    quiz = get_object_or_404(Quiz, quiz_uuid=quiz_uuid)
    context = {
        'page_title': "Start Quiz",
        'quiz': quiz
    }
    return render(request, template_name, context)


def stop_quiz(request, quiz_uuid):
    template_name = "quiz/quiz_stop.html"
    quiz = get_object_or_404(Quiz, quiz_uuid=quiz_uuid)
    context = {
        'page_title': "Stop Quiz",
    }
    return render(request, template_name, context)


def quiz_detail_uid(request, quiz_uuid):
    template_name = "quiz/quiz.html"
    context = {
        'page_title': "New Quiz",
    }
    return render(request, template_name, context)


def quiz_detail(request, slug):
    template_name = "quiz/quiz.html"
    quiz = get_object_or_404(Quiz, slug=slug)
    context = {
        'page_title': "Quiz",
        'quiz': quiz
    }
    return render(request, template_name, context)