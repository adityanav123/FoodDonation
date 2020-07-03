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
    user_type = models.IntegerField(null = True) # 0 - Donor 1 - Reciever
    #user_type = models.ChoiceField(choices = CHOICES, widget = models.RadioSelect)
    def __str__(self):
        return self.username