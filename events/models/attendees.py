from django.db import models

from .events import Events


class Attendee(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Blocked', 'Blocked'),
    ]

    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='attendees')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    phone_number = models.CharField(max_length=15, null=True)
    date_of_birth = models.DateField(null=False)
    registered_at = models.DateTimeField(auto_now_add=True)
    registration_data = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        ordering = ['-registered_at']
        verbose_name = 'Attendee'
        verbose_name_plural = 'Attendees'
        unique_together = ['event', 'email']