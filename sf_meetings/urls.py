from django.urls import path, re_path
from django.views.generic import RedirectView

from . import views
from .views import profile_views

urlpatterns = [
    path('profile/', profile_views.profile_view, name='profile'),
    path('profile/edit/', profile_views.edit_profile, name='profile_edit'),
    re_path(r'^$', RedirectView.as_view(url='login/telegram/', permanent=False)), #надо потом добавть landing page
    path('meetings-map/', views.map_view, name='meetings_map'), # Имя должно совпадать с используемым в href
    path('meetings-list/', views.list_view, name='meetings_list'),
    path('meeting-create/', views.create_view, name='meeting_create'),
    path('my-meetings/', views.my_meetings_view, name='my_meetings'),
    path('meeting/<int:meeting_id>/join/', views.join_meeting_view, name='join_meeting'),
    path('meeting/<int:pk>/', views.meeting_detail_view, name='meeting_detail'), # Или views.meeting_detail_view
    path('landing/', views.landing_view, name='landing'),
    # другие URL...
]