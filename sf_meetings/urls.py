from django.urls import path
from . import views

urlpatterns = [
    path('meetings-map/', views.map_view, name='meetings_map'), # Имя должно совпадать с используемым в href
    path('meetings-list/', views.list_view, name='meetings_list'),
    path('meeting-create/', views.create_view, name='meeting_create'),
    path('profile/', views.profile_view, name='profile_view'),
    # другие URL...
]