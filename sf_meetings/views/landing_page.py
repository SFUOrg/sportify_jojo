from django.shortcuts import render

def landing_view(request):
    return render(request, 'sf_meetings/landing_page.html')
