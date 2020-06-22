from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name = 'portal_index'),
    path('register', views.register, name = 'register')   
]
