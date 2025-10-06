from django.shortcuts import render

def profile_view(request):
    context = {
        'active_page': 'profile',
    }
    return render(request, 'sf_meetings/profile.html', context)