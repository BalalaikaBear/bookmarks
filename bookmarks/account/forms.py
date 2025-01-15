from django import forms
from django.contrib.auth import get_user_model
from .models import Profile


class LoginForm(forms.Form):
    """Форма входа на сайт"""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)  # прорисовка HTML-элемента password


class UserRegistrationForm(forms.ModelForm):
    """Форма регистрации"""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()  # модель User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        """Проверка на совпадение повторного (проверочного) пароля"""
        cd = self.cleaned_data
        if cd['password'] != cd['password']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    """Форма редактирования основных данных пользователя auth"""

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']


class ProfileEditForm(forms.ModelForm):
    """Форма редактирования дополнительных данных пользователя Profile"""

    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
