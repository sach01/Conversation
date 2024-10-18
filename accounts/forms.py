from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating new users. Inherits from Django's UserCreationForm.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'email']

class CustomUserLoginForm(AuthenticationForm):
    """
    Form for user login.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


'''
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')
'''