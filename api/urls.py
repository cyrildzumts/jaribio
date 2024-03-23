from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as drf_api_views
from api import views

app_name = 'api'
router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', drf_api_views.obtain_auth_token, name='api-token-auth'),
    path('authenticate/', views.authenticate, name='authenticate'),
    path('create-quiz/', views.create_quiz, name="create-quiz"),
    path('update-quiz/<uuid:quiz_uuid>/', views.update_quiz, name="update-quiz"),
    path('quizzes/<uuid:quiz_uuid>/create-question/', views.create_question, name="create-question"),
    path('quizzes/<uuid:quiz_uuid>/create-quizstep/', views.create_quizstep, name="create-quizstep"),
     path('quizzes/<uuid:quiz_uuid>/update-quizstep/<int:quizstep_id>/', views.update_quizstep, name="update-quizstep"),
    path('quizzes/<slug:quiz_slug>/questions/<uuid:question_uuid>/update/', views.update_question, name="update-question"),
    #path('quizzes/<uuid:quiz_slug>/questions/<uuid:question_uuid>/', views.question_details, name="question-details"),
    path('user-search/', views.UserSearchView.as_view(), name="user-search"),
]