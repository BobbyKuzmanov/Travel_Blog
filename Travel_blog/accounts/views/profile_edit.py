from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Travel_blog.accounts.forms.profile_edit import EditProfileForm
from Travel_blog.accounts.models import Profile
import os


@login_required
def edit_profile(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # If there's a new file being uploaded and an old file exists
            if 'profile_image' in request.FILES and profile.profile_image:
                # Delete the old file
                if os.path.isfile(profile.profile_image.path):
                    os.remove(profile.profile_image.path)
            
            form.save()
            return redirect('current user profile')
    else:
        form = EditProfileForm(instance=profile)

    context = {
        'user': user,
        'profile_form': form,
    }
    return render(request, 'accounts/profile_edit.html', context)
