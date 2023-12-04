from django import forms
from allauth.account.forms import EmailVerificationForm
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



class EmailVerificationForm(forms.ModelForm):

    code = forms.CharField(max_length=4)
    def clean_code(self):
        code = self.cleaned_data['code']
        # Add your verification logic here, e.g., comparing the code with the one stored in the database
        if code != stored_verification_code:
            raise forms.ValidationError("Invalid verification code")
        return code
