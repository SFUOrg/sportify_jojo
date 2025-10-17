from django.urls import path
from . import views
from .api import JoinMeetingView, LeaveMeetingView

urlpatterns = [
    path('meetings/create/', views.create_meeting_api, name='api_create_meeting'),
    path('meetings/', views.list_meetings_api, name='api_list_meetings'),
    path('meetings/<int:pk>/', views.meeting_detail_api, name='api_meeting_detail'),
    path('meetings/<int:pk>/delete/', views.delete_meeting_api, name='api_delete_meeting'),
    path('meetings/join/', JoinMeetingView.as_view(), name='api_join_meeting'),
    path('meetings/leave/', LeaveMeetingView.as_view(), name='api_leave_meeting'),
]