from django.forms.models import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from quiz.models import Answer, Question, Quiz, QuizStep
from quiz import constants as QUIZ_CONSTANTS
from quiz import quiz_service
from jaribio import utils
# Create your views here.


def quiz_home(request):
    template_name = "quiz/quiz_home.html"
    context = {
        'page_title': "Quiz Home",
        'quizzes': Quiz.objects.all()
    }
    return render(request, template_name, context)

@login_required
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


@login_required
def update_quiz(request, quiz_uuid):
    template_name = "quiz/quiz_update.html"
    quiz = get_object_or_404(Quiz, quiz_uuid=quiz_uuid)
    
    if request.method == QUIZ_CONSTANTS.REQUEST_METHOD_POST:
        try:
            results = quiz_service.update_quiz(quiz, utils.get_postdata(request))
            messages.success(request, "Quiz updated")
            return redirect(quiz)
        except Exception as e:
            messages.error(request, "Quiz not updated")

    context = {
        'page_title': "Update Quiz",
        'quiz': quiz,
        'QUIZ_TYPES' : QUIZ_CONSTANTS.QUIZ_TYPES,
        'DESCRIPTION_MAX_SIZE' : QUIZ_CONSTANTS.DESCRIPTION_MAX_SIZE
    }
    return render(request, template_name, context)

@login_required
def update_question(request, quiz_slug ,question_uuid):
    template_name = "quiz/question_update.html"
    question = get_object_or_404(Question, question_uuid=question_uuid)
    quiz = get_object_or_404(Quiz, slug=quiz_slug)
    AnswerFormset = inlineformset_factory(Question, Answer, fields=('content', 'is_correct'),extra=0, can_delete=False)
    formset = AnswerFormset(instance=question)
    context = {
        'page_title': "Update Question",
        'question': question,
        'quiz': quiz,
        'formset': formset,
        'QUESTION_TYPES': QUIZ_CONSTANTS.QUESTION_TYPES,
        'DESCRIPTION_MAX_SIZE' : QUIZ_CONSTANTS.DESCRIPTION_MAX_SIZE,
        'QUESTION_TYPE_MCQ' : QUIZ_CONSTANTS.QUESTION_TYPE_MCQ
    }
    return render(request, template_name, context)




@login_required
def delete_quiz(request, quiz_uuid):
    quiz = get_object_or_404(Quiz, quiz_uuid=quiz_uuid)
    Quiz.objects.filter(pk=quiz.pk).delete()
    return redirect('quiz:quiz-home')

@login_required
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


@login_required
def delete_question(request, question_uuid):
    question = get_object_or_404(Question, question_uuid=question_uuid)
    quiz = question.quiz
    Question.objects.filter(pk=question.pk).delete()
    return redirect(quiz)


@login_required
def create_quizstep(request, quiz_uuid):
    template_name = "quiz/quizstep_create.html"
    quiz = get_object_or_404(Quiz, quiz_uuid=quiz_uuid)
    context = {
        'page_title': "New QuizStep",
        'quiz': quiz,
        'questions': quiz.questions.all(),
        'SCORE_TYPES': QUIZ_CONSTANTS.ANSWER_SCORE_TYPES,
        'ANSWER_SCORE_STANDARD': QUIZ_CONSTANTS.ANSWER_SCORE_STANDARD
    }
    return render(request, template_name, context)




@login_required
def create_quizstep(request, quiz_uuid):
    template_name = "quiz/quizstep_create.html"
    quiz = get_object_or_404(Quiz, quiz_uuid=quiz_uuid)
    context = {
        'page_title': "New QuizStep",
        'quiz': quiz,
        'questions': quiz.questions.all(),
        'SCORE_TYPES': QUIZ_CONSTANTS.ANSWER_SCORE_TYPES,
        'ANSWER_SCORE_STANDARD': QUIZ_CONSTANTS.ANSWER_SCORE_STANDARD
    }
    return render(request, template_name, context)


@login_required
def quizstep_details(request, pk):
    template_name = "quiz/quizstep_details.html"
    quizstep = get_object_or_404(QuizStep, pk=pk)        
            
    context = {
        'page_title': "QuizStep",
        'quizstep': quizstep,
        'quiz': quizstep.quiz,
        'questions': quizstep.questions,
        'SCORE_TYPES': QUIZ_CONSTANTS.ANSWER_SCORE_TYPES,
        'ANSWER_SCORE_STANDARD': QUIZ_CONSTANTS.ANSWER_SCORE_STANDARD
    }
    return render(request, template_name, context)


@login_required
def update_quizstep(request, pk):
    template_name = "quiz/quizstep_update.html"
    quizstep = get_object_or_404(QuizStep, pk=pk)
    
    if request.method == QUIZ_CONSTANTS.REQUEST_METHOD_POST:
        try:
            results = quiz_service.update_quizstep(quizstep, utils.get_postdata(request))
            messages.success(request, "QuizStep updated")
            return redirect(quizstep.quiz)
        except Exception as e:
            messages.error(request, "Quiz not updated")
            
            
    context = {
        'page_title': "Update QuizStep",
        'quizstep': quizstep,
        'quiz': quizstep.quiz,
        'selected_questions': quizstep.questions,
        'questions': quizstep.quiz.questions.all(),
        'SCORE_TYPES': QUIZ_CONSTANTS.ANSWER_SCORE_TYPES,
        'ANSWER_SCORE_STANDARD': QUIZ_CONSTANTS.ANSWER_SCORE_STANDARD
    }
    return render(request, template_name, context)


@login_required
def delete_quizstep(request, quiz_slug, pk):
    quizstep = get_object_or_404(QuizStep, pk=pk)
    quiz = quizstep.quiz
    QuizStep.objects.filter(pk=quizstep.pk).delete()
    return redirect(quiz)



def start_quiz(request, quiz_uuid):
    template_name = "quiz/quiz_start.html"
    quiz = get_object_or_404(Quiz, quiz_uuid=quiz_uuid)
    context = {
        'page_title': "Start Quiz",
        'quiz': quiz
    }
    return render(request, template_name, context)



def play_quiz(request, quiz_slug, step):
    template_name = "quiz/play_step.html"
    quiz = get_object_or_404(Quiz, slug=quiz_slug)
    quiz_step = None
    questions = []
    try:
        quiz_step = QuizStep.objects.filter(quiz=quiz, rank=step).get()
        q_ids = list(map(lambda x: int(x), quiz_step.questions.split(',')))
        questions = [ Question.objects.get(pk=pk) for pk in q_ids]
    except QuizStep.DoesNotExist:
        pass
    
    context = {
        'page_title': "Start Quiz",
        'quiz': quiz,
        'questions': questions,
        'question': questions[0],
        'quizstep': quiz_step
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
    questions = quiz.questions.all()
    quizsteps = quiz.quiz_steps.all()
    context = {
        'page_title': "Quiz",
        'quiz': quiz,
        'questions': questions,
        'quizsteps': quizsteps
    }
    return render(request, template_name, context)


def question_details(request,quiz_slug, question_uuid):
    template_name = "quiz/question.html"
    question = get_object_or_404(Question, question_uuid=question_uuid)
    quiz = get_object_or_404(Quiz, slug=quiz_slug)
    AnswerFormset = inlineformset_factory(Question, Answer, fields=('content', 'is_correct', 'question'), extra=0, can_delete=False)
    formset = AnswerFormset(instance=question)
    context = {
        'page_title': "Update Question",
        'question': question,
        'quiz': quiz,
        'formset': formset,
        'QUESTION_TYPES': QUIZ_CONSTANTS.QUESTION_TYPES,
        'DESCRIPTION_MAX_SIZE' : QUIZ_CONSTANTS.DESCRIPTION_MAX_SIZE,
        'QUESTION_TYPE_MCQ' : QUIZ_CONSTANTS.QUESTION_TYPE_MCQ
    }
    return render(request, template_name, context)




def quiz_party(request, slug):
    template_name = "quiz/quiz_party.html"
    quiz = get_object_or_404(Quiz, slug=slug)
    context = {
        'page_title': "Quiz",
        'quiz': quiz,
    }
    return render(request, template_name, context)