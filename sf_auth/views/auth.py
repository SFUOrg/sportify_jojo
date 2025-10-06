from django.shortcuts import render

def login_view(request):
    return render(request, 'sf_auth/login.html')
