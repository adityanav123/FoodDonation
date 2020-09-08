from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'donor', 'reciever', 'organisation' ,'resources', 'locality', 'city', 'pin_code', 'state', 'contact_no')
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'donor', 'reciever', 'organisation' ,'resources', 'locality', 'city', 'pin_code', 'state', 'contact_no')

