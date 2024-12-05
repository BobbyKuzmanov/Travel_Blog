from django.contrib.auth import login
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from Travel_blog.accounts.forms.profile import ProfileForm
from Travel_blog.accounts.forms.signup import SignupForm


@transaction.atomic()
def signup_user(request):
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        
        if signup_form.is_valid() and profile_form.is_valid():
            # Create the user
            user = signup_form.save()
            
            # Create the profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            # Log the user in
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created successfully.')
            return redirect('current user profile')
        else:
            # If forms are invalid, return the same forms with errors
            messages.error(request, 'Please correct the errors below.')
    else:
        signup_form = SignupForm()
        profile_form = ProfileForm()
    
    context = {
        'signup_form': signup_form,
        'profile_form': profile_form,
    }
    return render(request, 'auth/signup.html', context)
