from django import forms
from django.contrib.auth import get_user_model
from Travel_blog.accounts.models import Profile

UserModel = get_user_model()


class EditUserCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = UserModel
        fields = ('username',)


class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'about_me', 'profile_image')
