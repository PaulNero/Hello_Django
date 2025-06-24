from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms


class CreateUserForm(UserCreationForm):
    nickname = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ['nickname', 'password1', 'password2']

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if Profile.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError('Этот никнейм уже занят.')
        return nickname


    def save(self, commit=True):
        user = super().save(commit=False)
        nickname = self.cleaned_data['nickname']
        user.username = nickname #кладём никнейм как юзер нейм в базовую модель авторизации в джанге
        if commit:
            user.save()
            Profile.objects.create(user=user, nickname=nickname)
        return user


    # class Meta:
    #     model = get_user_model()
    #     fields = ('nickname', 'password', 'password confirm')

    # def clean_password2(self):
    #     password1 = self.cleaned_data["password"]
    #     password2 = self.cleaned_data["password confirm"]
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError(
    #             self.error_messages['password_mismatch'],
    #             code='password_mismatch')
    #     return password2

    # def clean_nickname(self):
    #     nickname = self.cleaned_data.get("nickname")
    #     if nickname and get_user_model().objects.filter(nickname=nickname).exists():
    #         raise forms.ValidationError(
    #             self.error_messages['nickname_exists'],
    #             code='nickname_exists',
    #         )
    #     return nickname
        