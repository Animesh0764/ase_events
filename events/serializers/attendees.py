from rest_framework import serializers

from ..models.attendees import Attendee
from ..models.registration import RegistrationQuestions


class AttendeeSerializer(serializers.ModelSerializer):
    # registration_data = serializers.JSONField()
    class Meta:
        model = Attendee
        fields = ['id', 'event', 'name', 'email', 'status', 'date_of_birth', 'registered_at', 'phone_number','registration_data']

    def validate(self, data):
        event = data.get('event')
        registration_data = data.get('registration_data', {})

        ques = RegistrationQuestions.objects.filter(event=event)

        for que in ques:
            ques_id = str(que.id)
            if que.is_required and ques_id not in registration_data:
                raise serializers.ValidationError({'registration_data': f'{que.question_text} is required'})
        return data
    
    def create(self, validated_data):
        registration_data = validated_data.pop('registration_data')
        attendee = Attendee.objects.create(**validated_data)
        attendee.registration_data = registration_data
        attendee.save()
        return attendee
    
    def validate_status(self, value):
        if value not in dict(Attendee.STATUS_CHOICES):
            raise serializers.ValidationError("Invalid status choice.")
        return value