
from rest_framework import serializers
from django.contrib.auth.models import User
from quiz.models import Question, QuizImage, QuizSession,Quiz, Category, QuizStep, Answer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = Quiz.FORM_FIELDS


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = Question.FORM_FIELDS



class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = Answer.FORM_FIELDS



class QuizStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizStep
        fields = QuizStep.FORM_FIELDS


class QuizSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizSession
        fields = QuizSession.FORM_FIELDS



class QuizImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizImage
        fields = QuizImage.FORM_FIELDS


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = Category.FORM_FIELDS