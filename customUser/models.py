from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pin_code = models.IntegerField(null = True)
    contact_no = models.IntegerField(null = True)
    resources = models.IntegerField(null = True) # no. of persons avability/requirement
    locality = models.CharField(max_length = 100)
    city = models.CharField(max_length = 50)
    """CHOICES=[('0','Donor'),
                   ('1','Reciever')]"""
    state = models.CharField(max_length = 50, default = " ")
    user_type = models.IntegerField(null = True) # 0 - Donor 1 - Reciever
    email = models.EmailField(unique=True)
    #user_type = models.ChoiceField(choices = CHOICES, widget = models.RadioSelect)
    def __str__(self):
        return self.username


class Messages(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name = 'senders')
    reciever = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name = 'recievers')
    message = models.CharField(max_length = 150)
    read_unread = models.BooleanField(default = "False") # FALSE - UNREAD
    def __str__(self):
        return self.message