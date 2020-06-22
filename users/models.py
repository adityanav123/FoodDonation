from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    users = models.OneToOneField(User, on_delete = models.CASCADE)
    requirement = models.IntegerField()
    locality = models.TextField()
    def __str__(self):
        return f'{self.users.username} Profile'
