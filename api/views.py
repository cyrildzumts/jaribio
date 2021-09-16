from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.generics import ListAPIView
from api.serializers import UserSerializer
from quiz import quiz_service
from jaribio import utils


import logging
import uuid
logger = logging.getLogger(__name__)
# Create your views here.


class UserSearchByNameView(ListAPIView):
     #permission_classes = [IsAuthenticated]
     serializer_class = UserSerializer
     search_fields = ['last_name', 'first_name','username']
     filter_backends = [filters.SearchFilter]
     queryset = User.objects.filter(is_superuser=False)
     """
     def get_queryset(self):
          user_search = self.request.POST.get('user-search', "")
          if len(user_search) > 0 :
               return UserSerializer.Meta.model.objects.filter(last_name__icontains=user_search)
          return UserSerializer.Meta.model.objects.none()
     """


class UserSearchView(ListAPIView):
     #permission_classes = [IsAuthenticated]
     serializer_class = UserSerializer
     search_fields = ['last_name', 'first_name', 'username']
     filter_backends = [filters.SearchFilter]
     queryset = User.objects.filter(is_superuser=False)
     """
     def get_queryset(self):
          user_search = self.request.POST.get('user-search', "")
          if len(user_search) > 0 :
               return UserSerializer.Meta.model.objects.filter(last_name__icontains=user_search)
          return UserSerializer.Meta.model.objects.none()
    """


@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def authenticate(request):
    logger.debug("Received authenticate request")
    postdata = request.POST.copy()
    token = uuid.uuid4()
    return Response(data={"tokenType": 'Bearer', 'accessToken': token}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_quiz(request):
    postdata = utils.get_postdata(request)
    quiz = quiz_service.create_quiz(postdata)
    status_result = status.HTTP_200_OK
    if quiz:
        data = {'success': True, 'title': quiz.title, 'url': quiz.get_absolute_url()}
    else:
        status_result = status.HTTP_400_BAD_REQUEST
        data = {'success': False, 'error': 'Bad request'}
    return Response(data,status=status_result)


@api_view(['POST'])
def create_question(request, quiz_uuid):
    postdata = utils.get_postdata(request)
    question = quiz_service.create_question(postdata)
    status_result = status.HTTP_200_OK
    if question:
        data = {'success': True,'title': question.quiz.title, 'url': question.quiz.get_absolute_url()}
    else:
        status_result = status.HTTP_400_BAD_REQUEST
        data = {'success': False, 'error': 'Bad request'}
    return Response(data,status=status_result)


@api_view(['POST'])
def create_answer(request, question_uuid):
    postdata = utils.get_postdata(request)
    answer = quiz_service.create_answer(postdata)
    status_result = status.HTTP_200_OK
    if answer:
        data = {'success': True, 'title': answer.question.quiz.title, 'url': answer.question.quiz.get_absolute_url()}
    else:
        status_result = status.HTTP_400_BAD_REQUEST
        data = {'success': False, 'error': 'Bad request'}
    return Response(data,status=status_result)
