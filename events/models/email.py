from django.db import models

from .events import Events


class Email(models.Model):
    OPTION_CHOICES = [
        ('registration', 'Registration Mail'),
        ('24hr_reminder', '24 Hours Reminder'),
        ('1hr_reminder', '1 Hour Reminder'),
    ]

    option = models.CharField(max_length=20, choices=OPTION_CHOICES, unique=True, default='registration')
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='email', null=True)
    recipients = models.TextField(help_text="Comma-separated list of email addresses")
    subject = models.CharField(max_length=200, default="You have registered for")
    body = models.TextField(default="Hello, \n\n See you at the event!")
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email sent to {self.recepient} at {self.sent_at}"
    
    def recipients_list(self):
        return self.recipients.split(',')