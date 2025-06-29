from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms


class CreateUserForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True)

    class Meta:
        model = Profile
        fields = ['username', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control"}),
            'password1': forms.PasswordInput(attrs={"class": "form-control"}),
            'password2': forms.PasswordInput(attrs={"class": "form-control"}),
        }

        labels = {
            'username':'Enter Username',
            'password1':'Enter password',
            'password2':'Enter password',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Profile.objects.filter(username=username).exists():
            raise forms.ValidationError('Этот никнейм уже занят.')
        return username


    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     username = self.cleaned_data['username']
    #     user.username = username #кладём никнейм как юзер нейм в базовую модель авторизации в джанге
    #     if commit:
    #         user.save()
    #         Profile.objects.create(user=user, username=username)
    #     return user


    # class Meta:
    #     model = get_user_model()
    #     fields = ('username', 'password', 'password confirm')

    # def clean_password2(self):
    #     password1 = self.cleaned_data["password"]
    #     password2 = self.cleaned_data["password confirm"]
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError(
    #             self.error_messages['password_mismatch'],
    #             code='password_mismatch')
    #     return password2

    # def clean_username(self):
    #     username = self.cleaned_data.get("username")
    #     if username and get_user_model().objects.filter(username=username).exists():
    #         raise forms.ValidationError(
    #             self.error_messages['username_exists'],
    #             code='username_exists',
    #         )
    #     return username
        