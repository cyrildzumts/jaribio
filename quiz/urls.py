from django.conf.urls import include
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from quiz import views


app_name = "quiz"
quiz_patterns = [
    path('', views.quiz_home, name="quiz-home"),
    path('quiz-create/', views.create_quiz, name="quiz-create"),
    path('quiz/<uuid:quiz_uuid>/questions/create/', views.create_question, name="question-create"),
    path('quiz/<slug:quiz_slug>/questions/<uuid:question_uuid>/update/', views.update_question, name="question-update"),
    path('quiz/<slug:quiz_slug>/questions/<uuid:question_uuid>/delete/', views.delete_question, name="question-delete"),
    path('quiz/<slug:quiz_slug>/quizsteps/<int:pk>/delete/', views.delete_quizstep, name="quizstep-delete"),
    path('quiz/<slug:quiz_slug>/play/<int:step>/', views.play_quiz, name="play-quiz"),
    path('quiz/questions/<uuid:question_uuid>/', views.question_details, name="question-details"),
    path('quiz/<uuid:quiz_uuid>/quizsteps/create/', views.create_quizstep, name="quizstep-create"),
    path('quiz/<uuid:quiz_uuid>/update/', views.update_quiz, name="quiz-update"),
    path('quiz/<uuid:quiz_uuid>/delete/', views.delete_quiz, name="quiz-delete"),
    path('quiz/<slug:slug>/', views.quiz_detail, name="quiz-detail"),
    path('quiz-party/<slug:slug>/', views.quiz_party, name="quiz-party"),
    path('quiz/quizstep-details/<int:pk>/', views.quizstep_details, name="quizstep-details"),
    path('quiz/quizstep-update/<int:pk>/', views.update_quizstep, name="quizstep-update"),
    #path('quiz/quizstep-update/<int:pk>/', views.del, name="quizstep-delete"),
    #path('quiz/<uuid:quiz_uuid>/', views.quiz_detail, name="quiz-detail"),
    path('quiz/<uuid:quiz_uuid>/start/', views.start_quiz, name="quiz-start"),
    path('quiz/<uuid:quiz_uuid>/stop/', views.stop_quiz, name="quiz-stop"),

]

urlpatterns = [
    path('', include(quiz_patterns)),
    path('category/<slug:category_slug>/', include((quiz_patterns, app_name), namespace='category'))
]
