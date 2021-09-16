from django.conf.urls import url, include
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from quiz import views


app_name = "quiz"
quiz_patterns = [
    path('', views.quiz_home, name="quiz-home"),
    path('quiz-create/', views.create_quiz, name="quiz-create"),
    path('quiz/<uuid:quiz_uuid/questions/create/', views.create_question, name="question-create"),
    path('quiz/<uuid:quiz_uuid/quizsteps/create/', views.create_quizstep, name="quizstep-create"),
    path('quiz/<uuid:quiz_uuid>/update/', views.update_quiz, name="quiz-update"),
    path('quiz/<uuid:quiz_uuid>/delete/', views.delete_quiz, name="quiz-delete"),
    path('quiz/<slug:slug>/', views.quiz_detail, name="quiz-detail"),
    #path('quiz/<uuid:quiz_uuid>/', views.quiz_detail, name="quiz-detail"),
    path('quiz/<uuid:quiz_uuid>/start/', views.start_quiz, name="quiz-start"),
    path('quiz/<uuid:quiz_uuid>/stop/', views.stop_quiz, name="quiz-stop"),

]

urlpatterns = [
    path('', include(quiz_patterns)),
    path('category/<slug:category_slug>/', include((quiz_patterns, app_name), namespace='category'))
]
