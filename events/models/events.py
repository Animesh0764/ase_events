from datetime import datetime

# from community.models import Community
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class Events(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()

    # organizer = models.ForeignKey(DevHubUser, on_delete=models.CASCADE, related_name='organized_events')

    # Community = models.ForeignKey(
    #     Community,
    #     on_delete=models.CASCADE,
    #     related_name="events",
    #     blank=True,
    #     null=True,
    # )
    
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    timezone = models.CharField(max_length=50, default='GMT')

    is_online = models.BooleanField(default=False)
    online_link = models.URLField(blank=True, null=True)
    venue = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    is_registration_required = models.BooleanField(default=True)
    is_approval_required = models.BooleanField(default=False)
    ticket_type = models.CharField(
        max_length=10,
        choices=[('Free', 'Free'), ('Paid', 'Paid')],
        default='Free'
    )
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bulk_registration_allowed = models.BooleanField(default=False)
    max_tickets = models.IntegerField(default=0)
    capacity = models.PositiveIntegerField(default=200)
    is_registration_closed = models.BooleanField(default=False)

    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
    
    def is_upcoming(self):
        return self.start_datetime > datetime.now()
    
    def is_past(self):
        return self.end_datetime < datetime.now()
    
    def is_ongoing(self):
        return self.start_datetime <= datetime.now() and self.end_datetime >= datetime.now()
    
    def number_of_attendees(self):
        if not self.pk:
            return 0
        return self.attendees.count()

    @property
    def is_full(self):
        if not self.pk:
            return False
        return self.capacity - self.number_of_attendees() <= 0
        
    class Meta:
        ordering = ['-start_datetime']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def save(self, *args, **kwargs):
        #to avoid duplicate events in the same community
        # if self.status == 'Published':
        #     if Events.objects.filter(title = self.title, Community = self.Community).exists():
        #         raise ValidationError('Event already exists in this community')

        if self.bulk_registration_allowed and self.max_tickets is None:
            self.max_tickets = 20
        if self.ticket_type == 'Paid' and self.ticket_price is None:
            self.ticket_price = 100.0
        super().save(*args, **kwargs)

        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            
            # Ensure the slug is unique
            while Events.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        if not self.pk:
            super().save(*args, **kwargs)
        
        # Check if the event is full after saving
        if self.is_full:
            self.is_registration_required = True

        super().save(*args, **kwargs)
