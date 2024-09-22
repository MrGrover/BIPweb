from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Survey(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class SurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text


class SurveyAnswer(models.Model):
    question = models.ForeignKey(SurveyQuestion, related_name='answers', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_text = models.TextField()

    def __str__(self):
        return f"Answer by {self.user} to {self.question}"
