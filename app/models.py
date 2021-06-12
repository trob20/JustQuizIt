from django.db import models
from datetime import date, datetime
import re


class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData["first_name"]) < 2:
            errors["first_name"] = "First name should be at least 2 characters"

        if len(postData["last_name"]) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid email address"

        try:
            user = User.objects.get(email = postData['email'])
            errors["emailNotUnique"] = "Email already exists, enter a different email"
        except User.DoesNotExist:
            email = None

        if len(postData["password"]) < 8:
            errors["password"] = "Password should be at least 8 characters"

        if postData["password"] != postData["confirm_password"]:
            errors["password"] = "Passwords do not match"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    # quizzes_created - one-to-many
    # questions_created - one-to-many
    # quiz_history - one-to-many


class QuizManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData["name"]) is None:
            errors["name"] = "A quiz name must be provided!"
        elif len(postData["name"]) < 3:
            errors["name"] = "Quiz name must have at least 3 characters!"

class Quiz(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name = "quizzes_created", on_delete=models.CASCADE)
    objects = QuizManager()

    # questions - many-to-many


class QuestionManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData["question"]) is None:
            errors["question"] = "A question must be provided!"
        elif len(postData["question"]) < 3:
            errors["question"] = "Question must have at least 5 characters!"

        if len(postData["domain"]) is None:
            errors["domain"] = "A domain must be provided!"
        elif len(postData["domain"]) < 3:
            errors["domain"] = "A domain must have at least 3 characters!"


class Question(models.Model):
    source = models.CharField(max_length=10)
    source_name = models.CharField(max_length=25)
    technology = models.CharField(max_length=25)
    domain = models.CharField(max_length=50)
    question_type = models.CharField(max_length=20)
    question_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    question_created_by = models.ForeignKey(User, related_name = "questions_created", on_delete=models.CASCADE)
    related_quiz = models.ManyToManyField(Quiz, related_name = "questions", null=True)
    objects = QuestionManager()

    # answer_options - one-to-many


class AnswerOption(models.Model):
    answer_option = models.CharField(max_length=255)
    answer = models.CharField(max_length=10, default="Incorrect")
    related_question = models.ForeignKey(Question, related_name = "answer_options", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


#==========================================================
# Results
#==========================================================


class QuizTaken(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name = "quizzes_created", on_delete=models.CASCADE)

    # questions - many-to-many
    # quiz_taken - one-to-many


class QuestionTaken(models.Model):
    source = models.CharField(max_length=10)
    source_name = models.CharField(max_length=25)
    technology = models.CharField(max_length=25)
    domain = models.CharField(max_length=50)
    question_type = models.CharField(max_length=20)
    question_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    question_created_by = models.ForeignKey(User, related_name = "questions_created", on_delete=models.CASCADE)
    related_quiz = models.ManyToManyField(Quiz, related_name = "questions", null=True)
    # answer_options - one-to-many


class AnswerOptionTaken(models.Model):
    answer_option = models.CharField(max_length=255)
    answer = models.CharField(max_length=10, default="Incorrect")
    related_question = models.ForeignKey(Question, related_name = "answer_options", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # answer_selected - one-to-one


class AnswerSelected(models.Model):
    answer_selected = models.ForeignKey(AnswerOptionTaken, related_name="answer_selected", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class QuizHistory(models.Model):
    status = models.CharField(max_length=12)
    start_date = models.DateTimeField()
    completed_date = models.DateTimeField(null=True)
    quiz_taken_by = models.ForeignKey(User, related_name = "quiz_history", on_delete=models.CASCADE)
    quiz = models.ForeignKey(QuizTaken, related_name = "quiz_taken", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


#==========================================================
# Dropdowns
#==========================================================


class QuestionType(models.Model):
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Domain(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Correct(models.Model):
    name = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)