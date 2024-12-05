from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy


class SignOutView(LogoutView):
    next_page = reverse_lazy('index')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return redirect('index')
