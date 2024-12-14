from django.urls import path

from . import views

urlpatterns = [
    #list all events
    path('', views.ListAllEvents.as_view(), name='event_list'),

    #create event
    path('event/', views.EventCreationView.as_view(), name='event_creation'),

    #update a event
    path('update-event/<int:pk>/', views.EventCreationView.as_view(), name='event_update'),

    #list single event
    path('event/<int:pk>/', views.SingleEventView.as_view(), name='event_detail'),

    #delete event
    path('delete-event/<int:pk>/', views.DeleteEventView.as_view(), name='event_delete'),

    #email options
    path('events/<int:pk>/email/', views.SendEmailView.as_view(), name='email_options'),
    
    #send mail to attendees
    path('events/<int:pk>/send-mail/', views.SendEmailView.as_view(), name='send_mail'),

    #list all attendees
    path('event/<int:pk>/list-attendees/', views.ListAllAttendees.as_view(), name='attendees_list'),

    #update registration settings
    path('event/<int:pk>/update-registrations/', views.UpdateRegistrationsView.as_view(), name='update_registrations'),
    
    #get or post questions
    path('events/<int:pk>/questions/', views.RegistrationQuestionsView.as_view(), name='event-questions'),
    
    #update or delete questions
    path('events/<int:pk>/questions/<int:question_id>/', views.RegistrationQuestionsView.as_view(), name='event-question-detail'),

    #get questions for attendees
    path('events/<int:pk>/attendees/questions/', views.AttendeeRegistrationView.as_view(), name='attendee-questions'),

    #register attendees
    path('events/<int:pk>/attendees/', views.AttendeeRegistrationView.as_view(), name='register-attendee'),

    #update or delete attendee
    path('events/<int:pk>/update-attendees/<int:attendee_id>/', views.ManageAttendeesView.as_view(), name='attendee-detail'),
]