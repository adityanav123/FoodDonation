from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pin_code = models.IntegerField(null = False)
    contact_no = models.IntegerField(null = False)
    resources = models.IntegerField(null = False) # no. of persons avability/requirement
    locality = models.CharField(max_length = 100)
    city = models.CharField(max_length = 50)
    user_type = models.IntegerField(null = False) # 0 - Donor 1 - Reciever
    def __str__(self):
        return self.username