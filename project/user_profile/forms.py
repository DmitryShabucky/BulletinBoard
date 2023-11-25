from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        labels = {
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': "Фамилия",
        }
        empty_labels = {
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': "Фамилия",
        }
