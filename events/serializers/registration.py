from rest_framework import serializers

from ..models.events import Events
from ..models.registration import RegistrationQuestions


class RegistrationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = [
            'is_registration_required',
            'is_approval_required',
            'ticket_type',
            'ticket_price',
            'bulk_registration_allowed',
            'max_tickets',
            'capacity'
        ]

    def update(self, instance, validated_data):
        bulk_registration_allowed = validated_data.get('bulk_registration_allowed', instance.bulk_registration_allowed)
        ticket_type = validated_data.get('ticket_type', instance.ticket_type)

        if bulk_registration_allowed:
            validated_data['max_tickets'] = validated_data.get('max_tickets', 20)
        if ticket_type == 'Paid':
            validated_data['ticket_price'] = validated_data.get('ticket_price', 100)

        return super().update(instance, validated_data)

class RegistrationQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationQuestions
        fields = [
            'id',
            'event',
            'question_text',
            'is_required',
            'is_default'
        ]
        read_only_fields = ['is_default']