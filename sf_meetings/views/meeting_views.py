import json
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from sf_meetings.models import Meeting, SportCategory
from sf_meetings.forms import MeetingForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def map_view(request):
    meetings_data = []
    for meeting in Meeting.objects.all(): # Или используйте нужный QuerySet
        # Предположим, что у вашей модели есть поля latitude, longitude, title, description, date_time
        meeting_info = {
            'id': meeting.id,
            'latitude': meeting.latitude, # Убедитесь, что поле существует
            'longitude': meeting.longitude, # Убедитесь, что поле существует
            'title': meeting.title,
            'description': meeting.description or 'Без описания', # Или используйте поле date_time
            'date_time': meeting.date_time.strftime('%d.%m.%Y %H:%M') if meeting.date_time else 'Дата не указана', # Пример форматирования
            'detail_url': reverse('meeting_detail', kwargs={'pk': meeting.id}), # Генерируем URL заранее
        }
        meetings_data.append(meeting_info)

    context = {
        'meetings_json': json.dumps(meetings_data),
        'active_page': 'map', # или какое-то другое имя, соответствующее вашему bottom_menu.html
    }
    return render(request, 'sf_meetings/meetings_map.html', context)

def list_view(request):
    context = {
        'active_page': 'list', # Указываем, что это страница 'list'
    }
    return render(request, 'sf_meetings/meetings_list.html', context)

@login_required # Убедитесь, что пользователь аутентифицирован
def join_meeting_view(request, meeting_id):
    """
    Представление для присоединения пользователя к встрече.
    """
    meeting = get_object_or_404(Meeting, id=meeting_id)

    # Проверка, является ли пользователь уже участником
    if request.user in meeting.participants.all():
        messages.warning(request, f"Вы уже состоите в участниках встречи '{meeting.title}'.")
        return redirect('meeting_detail', pk=meeting.id) # Убедитесь, что 'meeting_detail' это имя URL для деталей встречи


    meeting.participants.add(request.user)

    messages.success(request, f"Вы успешно присоединились к встрече '{meeting.title}'.")

    return redirect('meeting_detail', pk=meeting.id)

# Или функциональное представление:
def meeting_detail_view(request, pk): # pk - это primary key встречи
    meeting = get_object_or_404(Meeting, pk=pk)
    context = {
        'meeting': meeting,
        'meeting_join_link': reverse('join_meeting', kwargs={'meeting_id': meeting.id}),
        'active_page': 'meetings', # Или какое-то другое имя
    }
    return render(request, 'sf_meetings/meeting_detail.html', context)

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

