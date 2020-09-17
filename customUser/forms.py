from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'donor', 'organisation' ,'resources', 'locality', 'city', 'pin_code', 'state', 'contact_no')
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'donor', 'organisation' ,'resources', 'locality', 'city', 'pin_code', 'state', 'contact_no')

class ContactUsForm(forms.Form):
	name = forms.CharField(max_length = 20)
	email = forms.EmailField()
	message = forms.CharField(widget = forms.Textarea)

class AnonymusUserForm(forms.Form):
    name = forms.CharField(max_length = 30)
    email = forms.EmailField(help_text = 'Please enter your valid email id, so that your request can be solved without issues.')
    resources = forms.IntegerField(help_text = 'For how many people do you want donation for?')
    message = forms.CharField(widget = forms.Textarea(attrs={'placeholder':'Please specify extra details. :) '}))


	