from django.urls import path, include
from Travel_blog.accounts.views.profile_edit import edit_profile
from Travel_blog.accounts.views.profile import profile
from Travel_blog.accounts.views.signout import SignOutView
from Travel_blog.accounts.views.signup import signup_user
from Travel_blog.accounts.views.signin import SignInView
from Travel_blog.accounts.views.profile_delete import delete_profile


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/', profile, name='current user profile'),
    path('profile/<int:pk>/', profile, name='user profile'),
    path('profile/edit/', edit_profile, name='edit profile'),
    path('profile/<int:pk>/delete/', delete_profile, name='delete profile'),
    path('signup/', signup_user, name='signup user'),
    path('signin/', SignInView.as_view(), name='signin user'),
    path('signout/', SignOutView.as_view(), name='signout user'),
]
