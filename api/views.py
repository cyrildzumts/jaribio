from django.shortcuts import get_object_or_404
from quiz.models import Question, Quiz, QuizStep
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
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
        data = {'success': True, 'title': quiz.title, 'message': 'Quiz created', 'url': quiz.get_absolute_url()}
    else:
        status_result = status.HTTP_400_BAD_REQUEST
        data = {'success': False, 'error': 'Bad request'}
    return Response(data,status=status_result)


@api_view(['POST'])
def update_quiz(request, quiz_uuid):
    logger.info(f"API update quiz Request from user {request.user.username}")
    data = None
    status_result = status.HTTP_200_OK
    try:
        quiz = get_object_or_404(Quiz, quiz_uuid=quiz_uuid)
        postdata = utils.get_postdata(request)
        result = quiz_service.update_quiz(quiz, postdata)
        data = result
    except Exception as e:
        status_result = status.HTTP_400_BAD_REQUEST
        data = {'success': False, 'message': 'Bad request'}

    return Response(data,status=status_result)


@api_view(['POST'])
def create_question(request, quiz_uuid):
    logger.info(f"API create question Request from user {request.user.username}")
    postdata = utils.get_postdata(request)
    question = quiz_service.create_question(postdata)
    status_result = status.HTTP_200_OK
    if question:
        data = {'success': True,'message': 'Question Created', 'url': ''}
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
        data = {'success': True, 'message': 'Answer Created', 'url': ''}
    else:
        status_result = status.HTTP_400_BAD_REQUEST
        data = {'success': False, 'error': 'Bad request'}
    return Response(data,status=status_result)


@api_view(['POST'])
def create_quizstep(request, quiz_uuid):
    postdata = utils.get_postdata(request)
    step = quiz_service.create_quizstep(postdata)
    status_result = status.HTTP_200_OK
    if step:
        data = {'success': True, 'message': 'QuizStep Created', 'url': step.quiz.get_absolute_url()}
    else:
        status_result = status.HTTP_400_BAD_REQUEST
        data = {'success': False, 'error': 'Bad request'}
    return Response(data,status=status_result)


@api_view(['POST'])
def update_quizstep(request, quiz_uuid, quizstep_id):
    status_result = status.HTTP_200_OK
    data = None
    logger.info(f"Updating QuizStep {quizstep_id} for Quiz {quiz_uuid}")
    try:
        quizstep = QuizStep.objects.get(pk=quizstep_id)
        results = quiz_service.update_quizstep(quizstep, utils.get_postdata(request))
        data = {'success': True, 'message': 'QuizStep Update', 'url': quizstep.get_absolute_url()}

    except Exception as e:
        status_result = status.HTTP_400_BAD_REQUEST
        data = {'success': False, 'error': 'Bad request'}
        logger.error(f"Error on updating QuizStep {quizstep_id} for Quiz {quiz_uuid} - Error {e}")
    return Response(data,status=status_result)


@api_view(['POST'])
def update_question(request, quiz_slug, question_uuid):
    postdata = utils.get_postdata(request)
    logger.info(f"API Question update request from user {request.user.username}")
    quiz = None
    question = None
    try:
        question = Question.objects.get(question_uuid=question_uuid)
        quiz = Quiz.objects.get(slug=quiz_slug)
    except ObjectDoesNotExist as e:
        logger.warn(f"API : Could not found question {quiz}[slug={quiz_slug}] or question {question}[uuid={question_uuid}")
        return Response({'success': False, 'message': 'Not found', 'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    results= quiz_service.update_question(question, postdata)
    status_result = status.HTTP_200_OK
    if results:
        data = {'success': True, 'message': 'updated', 'url': results['question'].get_absolute_url()}
    else:
        status_result = status.HTTP_400_BAD_REQUEST
        data = {'success': False, 'error': 'Bad request'}
    return Response(data,status=status_result)



@api_view(['GET'])
def quiz_data(request, quiz_uuid):
    logger.info(f"API fetch quiz data Request from user {request.user.username}")
    data = None
    status_result = status.HTTP_200_OK
    try:
        data = quiz_service.get_quiz_party_data(quiz_uuid)
    except Exception as e:
        status_result = status.HTTP_400_BAD_REQUEST
        data = {'success': False, 'message': 'Bad request'}

    return Response(data,status=status_result)