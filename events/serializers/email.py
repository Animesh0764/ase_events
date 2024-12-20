from typing import List

from django.core.mail import send_mass_mail
from django.utils import timezone
from rest_framework import serializers

from ..models.attendees import Attendee
from ..models.email import Email


class EmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Email
        fields = ['id', 'recipients', 'subject', 'body', 'sent_at', 'option']

    def get_recipients(self, value):
        return value.recipients_list()

    def validate(self, data):
        if 'subject' not in data:
            raise serializers.ValidationError({"subject": "Subject is required."})
        return data

    def send_mail(self, event):
        print("Validated data:", self.validated_data)
        self.is_valid(raise_exception=True)

        if not self.validated_data.get('recipients'):
            recipients = Attendee.objects.filter(event=event).values_list('email', flat=True)
            if not recipients:
                raise serializers.ValidationError("No attendees found for this event.")
        else:
            recipients = self.validated_data['recipients']

        subject = self.validated_data.get('subject', 'Default Subject')
        body = self.validated_data.get('body', 'Default Body')
        recipients = [r.strip() for r in recipients.split(',')]
        
        try:

            import resend

            resend.api_key = "re_8KWgEiWE_CR4851VCE5vbuLGpjh4xiUWB"

            for recipient in recipients:
                params: resend.Emails.SendParams = {
                    "from": "Test <onboarding@resend.dev>",
                    "to": [recipient],
                    "subject": subject,
                    "html": body
                }

            email = resend.Emails.send(params)
            print(email)

            # send_mass_mail([
            #     (subject, body, 'animeshsingh0704@gmail.com', [recipient]) for recipient in recipients
            # ])


            self.validated_data['sent_at'] = timezone.now()

        except Exception as e:
            raise serializers.ValidationError(str(e))
        
        