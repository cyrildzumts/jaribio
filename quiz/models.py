from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from quiz import constants as Constants
import uuid

# Create your models here.

def upload_to(instance, filename):
    return f"images/{instance.name}/{instance.height}x{instance.width}-{filename}"


class QuizImage(models.Model):
    height = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=64, null=False, blank=False)
    image = models.ImageField(upload_to=upload_to, height_field='height', width_field='width')
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    last_edited_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    image_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    FORM_FIELDS = ['name', 'image']


    def delete_image_file(self):
        self.image.delete(False)

    def get_image_url(self):
        return self.image.url
    
    def get_absolute_url(self):
        return reverse("quiz:quiz-image-detail", kwargs={"image_uuid": self.image_uuid})
    
    def get_dashboard_url(self):
        return reverse("dashboard:quiz-image-detail", kwargs={"image_uuid": self.image_uuid})
    
    def get_update_url(self):
        return reverse("dashboard:quiz-image-update", kwargs={"image_uuid": self.image_uuid})

    def get_delete_url(self):
        return reverse("dashboard:quiz-image-delete", kwargs={"image_uuid": self.image_uuid})


class Category(models.Model):
    name = models.CharField(max_length=64)
    display_name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addeds_categories', blank=False, null=False)
    is_active = models.BooleanField(default=True)
    view_count = models.IntegerField(blank=True, null=True, default=0)
    parent = models.ForeignKey('self', related_name='children', blank=True, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=Constants.DESCRIPTION_MAX_SIZE, blank=True, null=True)
    category_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    FORM_FIELDS = ['name', 'display_name', 'parent', 'added_by', 'is_active']

    def __str__(self):
        return f"{self.name} - {self.display_name}"

    
    def get_children(self):
        return Category.objects.filter(parent=self)
    
    def get_absolute_url(self):
        return reverse("quiz:category-detail", kwargs={"category_uuid": self.category_uuid})
    
    def get_slug_url(self):
        return reverse("quiz:category-detail", kwargs={"slug": self.slug})
    
    def get_dashboard_url(self):
        return reverse("dashboard:category-detail", kwargs={"category_uuid": self.category_uuid})
    
    def get_update_url(self):
        return reverse("dashboard:category-update", kwargs={"category_uuid": self.category_uuid})
    
    def get_delete_url(self):
        return reverse("dashboard:category-delete", kwargs={"category_uuid": self.category_uuid})
    


class Quiz(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quizzes')
    title = models.CharField(max_length=Constants.QUESTION_MAX_LENGTH)
    description = models.CharField(max_length=Constants.DESCRIPTION_MAX_SIZE)
    image = models.ForeignKey(QuizImage, blank=True, null=True, related_name="quizzes", on_delete=models.SET_NULL)
    max_questions = models.IntegerField(blank=True, null=True)
    quiz_type = models.IntegerField(default=Constants.QUIZ_TYPE_CHALLENGE, choices=Constants.QUIZ_TYPES)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    last_edited_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    player_count = models.IntegerField(blank=True, null=True, default=0)
    plays_count = models.IntegerField(blank=True, null=True, default=0)
    slug = models.SlugField(max_length=250, blank=True, null=True)
    quiz_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    FORM_FIELDS = ['title', 'description', 'image', 'max_questions', 'quiz_type', 'created_by']

    def __str__(self):
        return f"{self.tile}"

    def get_absolute_url(self):
        return reverse("quiz:quiz-detail", kwargs={"slug": self.slug})

    
    def get_dashboard_url(self):
        return reverse("dashboard:quiz-detail", kwargs={"quiz_uuid": self.quiz_uuid})
    
    def get_update_url(self):
        return reverse("quiz:quiz-update", kwargs={"quiz_uuid": self.quiz_uuid})
    
    def get_delete_url(self):
        return reverse("dashboard:quiz-delete", kwargs={"quiz_uuid": self.quiz_uuid})


class Question(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_questions')
    content = models.CharField(max_length=Constants.QUESTION_MAX_LENGTH)
    explanation = models.CharField(max_length=Constants.DESCRIPTION_MAX_SIZE, blank=True, null=True)
    answer_count = models.IntegerField(blank=True, null=True, default=1)
    score = models.IntegerField()
    question_type = models.IntegerField(default=Constants.QUESTION_TYPE_MCQ, choices=Constants.QUESTION_TYPES)
    
    image = models.ForeignKey(QuizImage, blank=True, null=True, related_name="questions", on_delete=models.SET_NULL)
    quiz = models.ManyToManyField(Quiz)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    last_edited_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    question_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    FORM_FIELDS = ['content','explanation','answer_count','score','image','quiz', 'created_by']



class Answer(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_answers')
    content = models.CharField(max_length=Constants.QUESTION_MAX_LENGTH)
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    last_edited_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    answer_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    FORM_FIELDS = ['content', 'question','is_correct', 'is_active', 'created_by']



class QuizSession(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="quiz_sessions", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='quiz_sessions', blank=True, null=True)
    session_key = models.CharField(max_length=64)
    score = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(blank=True, null=True)
    FORM_FIELDS = ['quiz', 'user', 'session_key', 'score']


class QuizStep(models.Model):
    title = models.CharField(max_length=64)
    quiz = models.ForeignKey(Quiz, related_name="quiz_steps", on_delete=models.CASCADE)
    questions = models.CharField(max_length=64)
    rank = models.IntegerField()
    score_type = models.IntegerField(blank=True, null=True, default=Constants.ANSWER_SCORE_STANDARD, choices=Constants.ANSWER_SCORE_TYPES)
    FORM_FIELDS = ['quiz', 'title', 'questions', 'score_type', 'rank']