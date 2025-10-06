from django.shortcuts import render, get_object_or_404
from sf_auth.models import Profile 

def profile_view(request):
    # Получаем профиль текущего пользователя
    profile = get_object_or_404(Profile, user=request.user)

    # Получаем связанные виды спорта
    interested_sports = profile.sport_categories.all()

    # Получаем встречи, в которых участвует пользователь через профиль (если это логично)
    # meetings = profile.meetings.all() # Пример, если нужно отображать встречи в профиле

    context = {
        'active_page': 'profile', # Для подсветки кнопки в меню
        'profile': profile,
        'interested_sports': interested_sports,
        # 'meetings': meetings, # Если нужно
    }
    return render(request, 'sf_meetings/profile.html', context)