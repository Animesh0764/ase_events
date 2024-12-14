from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.views import APIView

from .models.attendees import Attendee
from .models.email import Email
from .models.events import Events
from .models.registration import RegistrationQuestions
from .serializers.attendees import AttendeeSerializer
from .serializers.email import EmailSerializer
from .serializers.events import EventSerializer
from .serializers.registration import (
    RegistrationQuestionsSerializer,
    RegistrationSettingsSerializer,
)

# Create your views here.

class EventCreationView(APIView):
    #permission_classes = [IsAuthenticated]

    def post(self, req, *args, **kwargs):
        serializer = EventSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, req, pk=None):
        if not pk:
            return Response({"Error": "Event ID (pk) is required for updating."}, status=HTTP_400_BAD_REQUEST)
        event = get_object_or_404(Events, pk=pk)
        serializer = EventSerializer(event, data=req.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def patch(self, req, pk=None):
        if not pk:
            return Response({"Error": "Event ID (pk) is required for updating."}, status=HTTP_400_BAD_REQUEST)
        event = get_object_or_404(Events, pk=pk)
        serializer = EventSerializer(event, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class EventRegistrationView(APIView):
    #permission_classes = [IsAuthenticated]

    def post(self, req, *args, **kwargs):
        event_id = req.data.get('event_id')
        try:
            event = Events.objects.get(id=event_id)
        except:
            return Response({'Message': 'Event does not exist'}, status=HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(id=req.user.id)
        if Attendee.objects.filter(event=event, email=user.email).exists():
            return Response({'Message': 'You are already registered for this event'}, status=HTTP_400_BAD_REQUEST)
        
        if event.is_full:
            return Response({'Message': 'Event is full. Registration has been closed'}, status=HTTP_400_BAD_REQUEST)
        
        if event.is_registration_required:
            if event.is_approval_required:
                Attendee.objects.create(event=event, name=user.username, email=user.email, status='Pending')
                return Response({'Message': 'Registration successful. Your request is pending for approval'}, status=HTTP_201_CREATED)
            else:
                Attendee.objects.create(event=event, name=user.username, email=user.email, status='Approved')
                return Response({'Message': 'Registration successful. Your request is approved'}, status=HTTP_201_CREATED)
        else:
            return Response({'Message': 'Registration not required for this event'}, status=HTTP_400_BAD_REQUEST)

class ListAllEvents(APIView):

    def get(self, req):
        events = Events.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class SingleEventView(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, req, pk=None):
        try:
            event = Events.objects.get(id=pk)
        except:
            return Response({'Message': 'Event does not exist'}, status=HTTP_400_BAD_REQUEST)
        
        serializer = EventSerializer(event)
        return Response(serializer.data, status=HTTP_200_OK)

class ListAllAttendees(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, req, pk = None):
        attendees = Attendee.objects.filter(event_id = pk)
        if not attendees.exists():
            return Response({"error": "No attendees found for this event."}, status=HTTP_404_NOT_FOUND)

        serializer = AttendeeSerializer(attendees, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class UpdateRegistrationsView(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, req, pk=None):
        try:
            event = Events.objects.get(id=pk)
        except Events.DoesNotExist:
            return Response({"error": "Event not found."}, status=HTTP_400_BAD_REQUEST)

        serializer = RegistrationSettingsSerializer(event)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def patch(self, req, pk=None):
        try:
            event = Events.objects.get(id=pk)
        except Events.DoesNotExist:
            return Response({"error": "Event not found."}, status=HTTP_400_BAD_REQUEST)

        serializer = RegistrationSettingsSerializer(event, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
class RegistrationQuestionsView(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, req, pk=None, question_id=None):
        try:
            event = Events.objects.get(id=pk)
        except Events.DoesNotExist:
            return Response({"error": "Event not found."}, status=HTTP_400_BAD_REQUEST)
        questions = RegistrationQuestions.objects.filter(event=event)
        serializer = RegistrationQuestionsSerializer(questions, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def post(self, req, pk=None, question_id=None):
        try:
            event = Events.objects.get(id=pk)
        except Events.DoesNotExist:
            return Response({"error": "Event not found."}, status=HTTP_400_BAD_REQUEST)
        
        data = req.data.copy()
        data['event'] = event.id
        serializer = RegistrationQuestionsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def patch(self, req, pk=None, question_id=None):
        try:
            event = Events.objects.get(id=pk)
        except Events.DoesNotExist:
            return Response({"error": "Event not found."}, status=HTTP_400_BAD_REQUEST)
        try:
            question = RegistrationQuestions.objects.get(id=question_id)
        except RegistrationQuestions.DoesNotExist:
            return Response({"error": "Question not found."}, status=HTTP_400_BAD_REQUEST)
        
        serializer = RegistrationQuestionsSerializer(question, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, req, pk=None, question_id=None):
        try:
            event = Events.objects.get(id=pk)
        except Events.DoesNotExist:
            return Response({"error": "Event not found."}, status=HTTP_400_BAD_REQUEST)
        try:
            question = RegistrationQuestions.objects.get(id=question_id)
        except RegistrationQuestions.DoesNotExist:
            return Response({"error": "Question not found."}, status=HTTP_400_BAD_REQUEST)
        
        question.delete()
        return Response({"message": "Question deleted successfully"}, status=HTTP_200_OK)
    
class AttendeeRegistrationView(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, req, pk=None):
        try:
            event = Events.objects.get(id=pk)
        except Events.DoesNotExist:
            return Response({"error": "Event not found."}, status=HTTP_404_NOT_FOUND)

        questions = RegistrationQuestions.objects.filter(event=event)
        serializer = RegistrationQuestionsSerializer(questions, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, req, pk=None):
        try:
            event = Events.objects.get(id=pk)
        except Events.DoesNotExist:
            return Response({"error": "Event not found."}, status=HTTP_404_NOT_FOUND)

        data = req.data.copy()
        data['event'] = event.id
        serializer = AttendeeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    
class DeleteEventView(APIView):
    #permission_classes = [IsAuthenticated]

    def delete(self, req, pk=None):
        if not pk:
            return Response({"Error": "Event ID (pk) is required for deletion."}, status=HTTP_400_BAD_REQUEST)
        event = get_object_or_404(Events, pk=pk)
        event.delete()
        return Response({"Message": "Event deleted successfully"}, status=HTTP_200_OK)

class ManageAttendeesView(APIView):
    #permission_classes = [IsAuthenticated]

    def patch(self, req, pk=None, attendee_id=None):
        try:
            event = Events.objects.get(id=pk)
        except Events.DoesNotExist:
            return Response({"error": "Event not found."}, status=HTTP_404_NOT_FOUND)
        
        try:
            attendee = Attendee.objects.get(id=attendee_id, event=event)
        except Attendee.DoesNotExist:
            return Response({"error": "Attendee not found."}, status=HTTP_404_NOT_FOUND)
        
        serializer = AttendeeSerializer(attendee, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, req, pk=None, attendee_id=None):
        try:
            event = Events.objects.get(id=pk)
        except Events.DoesNotExist:
            return Response({"error": "Event not found."}, status=HTTP_404_NOT_FOUND)
        
        try:
            attendee = Attendee.objects.get(id=attendee_id)
        except Attendee.DoesNotExist:
            return Response({"error": "Attendee not found."}, status=HTTP_404_NOT_FOUND)
        
        attendee.delete()
        return Response({"message": "Attendee deleted successfully"}, status=HTTP_200_OK)

class SendEmailView(APIView):
    #permission_classes = [IsAuthenticated]
    def get(self, req, pk=None):
        try:
            event = Events.objects.get(id=pk)
        except Events.DoesNotExist:
            return Response({"error": "Event not found."}, status=HTTP_404_NOT_FOUND)
        
        try:
            email = Email.objects.filter(event=event)
        except Email.DoesNotExist:
            return Response({"error": "Email not found."}, status=HTTP_404_NOT_FOUND)
        serializer = EmailSerializer(email, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, req, pk=None):
        serializer = EmailSerializer(data=req.data)
        if serializer.is_valid():
            try:
                event = Events.objects.get(id=pk)
                serializer.send_mail(event)
                return Response({"message": "Email sent successfully"}, status=HTTP_200_OK)
            except Events.DoesNotExist:
                return Response({"error": "Event not found."}, status=HTTP_404_NOT_FOUND)
            except serializers.ValidationError as e:
                return Response({"error": e.detail}, status=HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)