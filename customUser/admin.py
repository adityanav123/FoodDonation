from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'donor', 'receiver', 'organisation', 'resources', 'locality', 'city', 'state', 'pin_code', 'contact_no']

admin.site.register(CustomUser, CustomUserAdmin)

