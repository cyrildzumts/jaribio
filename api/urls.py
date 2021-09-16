from django.conf.urls import url, include
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
    path('user-search/', views.UserSearchView.as_view(), name="user-search"),
]