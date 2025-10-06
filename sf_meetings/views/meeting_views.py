from django.shortcuts import render
from sf_meetings.models import Meeting
def map_view(request):
    meetings = Meeting.objects.all() # Получаем все встречи
    context = {
        'active_page': 'map',
        'meetings': meetings, # Передаём в контекст
    }
    return render(request, 'sf_meetings/meetings_map.html', context)

def list_view(request):
    context = {
        'active_page': 'list', # Указываем, что это страница 'list'
    }
    return render(request, 'sf_meetings/meetings_list.html', context)

def create_view(request):
    context = {
        'active_page': 'create',
    }
    return render(request, 'sf_meetings/meeting_create.html', context)

