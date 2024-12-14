from rest_framework import serializers

from ..models.events import Events


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['id', 'title', 'description', 'start_datetime', 'end_datetime', 'timezone', 'is_online', 'online_link', 'venue', 'address','image', 'created_at', 'updated_at']

    def create(self, data):
        return Events.objects.create(**data)
    
    def update(self, instance, data):
        instance.title = data.get('title', instance.title)
        instance.description = data.get('description', instance.description)
        instance.start_datetime = data.get('start_datetime', instance.start_datetime)
        instance.end_datetime = data.get('end_datetime', instance.end_datetime)
        instance.timezone = data.get('timezone', instance.timezone)
        instance.is_online = data.get('is_online', instance.is_online)
        instance.online_link = data.get('online_link', instance.online_link)
        instance.venue = data.get('venue', instance.venue)
        instance.address = data.get('address', instance.address)
        instance.save()

        return instance

from django.core.exceptions import ValidationError


class EventDeleteSerializer(serializers.ModelSerializer):
    event_id = serializers.IntegerField()

    def validate(self, data):
        if not Events.objects.filter(id = data['event_id']).exists():
            raise ValidationError('Event does not exist')
        return data
    
    def delete(self, instance):
        event = Events.objects.get(id = instance['event_id'])
        event.delete()
        return {"Message": "Event deleted successfully"}