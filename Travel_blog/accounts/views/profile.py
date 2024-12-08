from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from Travel_blog.accounts.forms.profile import ProfileForm
from Travel_blog.app.models import Destination
from django.contrib import messages


@login_required
def profile(request, pk=None):
    # If no pk is provided, show current user's profile
    if pk is None:
        profile_user = request.user
        is_owner = True
    else:
        profile_user = get_object_or_404(User, pk=pk)
        is_owner = request.user == profile_user

    destinations = Destination.objects.filter(user_id=profile_user.id)
    if request.method == 'GET':
        context = {
            'profile_user': profile_user,  # The user whose profile we're viewing
            'destinations': destinations,
            'is_owner': is_owner,
        }
        return render(request, 'accounts/profile.html', context)
    else:
        if not is_owner:
            messages.error(request, "You cannot modify another user's profile.")
            return redirect('current user profile')
            
        form = ProfileForm(request.POST, request.FILES, instance=profile_user.profile)
        if form.is_valid():
            form.save()
            return redirect('current user profile')
        return redirect('current user profile')
