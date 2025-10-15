from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from sf_auth.models.profile import Profile
from sf_meetings.forms import ProfileForm

@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    interested_sports = profile.sport_categories.all()
    context = {
        'profile': profile,
        'interested_sports': interested_sports,
    }
    return render(request, 'sf_meetings/profile.html', context)

@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # имя url смотри в urls.py
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'sf_meetings/profile_edit.html', {'form': form})