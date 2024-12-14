from django.db import models

from .events import Events


class RegistrationQuestions(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=255)
    is_required = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)