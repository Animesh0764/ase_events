from django.db.models.signals import post_save
from django.dispatch import receiver

from .models.events import Events
from .models.registration import RegistrationQuestions


@receiver(post_save, sender=Events)
def create_default_questions(sender, instance, created, **kwargs):
    if created:
        default_questions = [
            {"question_text": "First Name", "is_required": True, "is_default": True},
            {"question_text": "Last Name", "is_required": True, "is_default": True},
            {"question_text": "Email", "is_required": True, "is_default": True},
            {"question_text": "Phone Number", "is_required": False, "is_default": True},
        ]

        for question in default_questions:
            RegistrationQuestions.objects.create(
                event=instance,
                **question
            )