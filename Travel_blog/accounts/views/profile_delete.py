from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User


@login_required
def delete_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.user == user:
        if request.method == 'POST':
            # This will trigger the Profile.delete() method we created
            user.profile.delete()
            # Delete the user account
            user.delete()
            # Log the user out
            logout(request)
            messages.success(request, 'Your profile has been successfully deleted.')
            return redirect('index')
        
        return render(request, 'profile_delete.html')
    else:
        return redirect('index')
