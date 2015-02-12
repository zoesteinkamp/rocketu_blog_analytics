from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail


class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)



    def save(self, commit=True):
        user = super(EmailUserCreationForm, self).save(commit=commit)
        send_mail('Hey there', 'Sign up', 'gkadillak@gmail.com', user.email, fail_silently=False)
        return user