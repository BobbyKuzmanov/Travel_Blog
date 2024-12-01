from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from Travel_blog.accounts.forms.signin import SignInForm


class SignInView(LoginView):
    template_name = "auth/signin.html"
    form_class = SignInForm
