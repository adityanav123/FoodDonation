from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'donor', 'receiver', 'organisation' ,'resources', 'locality', 'city', 'pin_code', 'state', 'contact_no')
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'donor', 'receiver', 'organisation' ,'resources', 'locality', 'city', 'pin_code', 'state', 'contact_no')

class ContactUsForm(forms.Form):
	name = forms.CharField(max_length = 20)
	email = forms.EmailField()
	message = forms.CharField(widget = forms.Textarea)
	