#from django.contrib.auth.models import User
from django import forms
from quiz.models import Answer, Question, QuizImage, QuizSession,Quiz, Category, QuizStep


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = Quiz.FORM_FIELDS


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = Category.FORM_FIELDS


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = Question.FORM_FIELDS



class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = Answer.FORM_FIELDS



class QuizStepForm(forms.ModelForm):
    class Meta:
        model = QuizStep
        fields = QuizStep.FORM_FIELDS


class QuizSessionForm(forms.ModelForm):
    class Meta:
        model = QuizSession
        fields = QuizSession.FORM_FIELDS



class QuizImageForm(forms.ModelForm):
    class Meta:
        model = QuizImage
        fields = QuizImage.FORM_FIELDS