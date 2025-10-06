from django.shortcuts import render, redirect
from sf_meetings.models import Meeting, SportCategory
from sf_meetings.forms import MeetingForm
from django.contrib import messages

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
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False) # Не сохраняем сразу
            meeting.organizer = request.user # Устанавливаем организатора
            meeting.save() # Теперь сохраняем
            messages.success(request, 'Мероприятие успешно создано!')
            return redirect('meetings_map') # Перенаправляем на список после создания
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = MeetingForm()

    context = {
        'form': form,
        'active_page': 'create', # Для подсветки меню
    }
    return render(request, 'sf_meetings/meeting_create.html', context)

