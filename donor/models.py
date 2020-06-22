'''from django.contrib.auth.models import User'''
from django.db import models
from django_google_maps import fields as map_fields


class Profile(models.Model):

    user = models.CharField(max_length=25, blank=True, null=True)
    email = models.EmailField(null=False)
    city = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    contact = models.PositiveIntegerField(max_length=10, blank=True, null=True)
    pincode = models.PositiveIntegerField(max_length=6, blank=True, null=True)
    resources = models.CharField(max_length=500)
    locality = models.CharField(max_length=300)
    '''geolocation = map_fields.GeoLocationField(max_length=100)'''

    def __str__(self):
        return self.user
