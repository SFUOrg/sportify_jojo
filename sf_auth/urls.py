from django.urls import path
from sf_auth.views import login_view

app_name = 'sf_auth'

urlpatterns = [
    path('telegram/', login_view, name='login'),
]