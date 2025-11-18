from django.urls import path
from .views import landing_view
from .api import JoinMeetingView, LeaveMeetingView

urlpatterns = [
    path('', landing_view, name='landing-page'),
    path('join/', JoinMeetingView.as_view(), name='join-meeting'),
    path('leave/', LeaveMeetingView.as_view(), name='leave-meeting'),
]