from django.urls import path
from . import views
urlpatterns = [
<<<<<<< HEAD
    path('', views.index, name='portalIndex'),
=======
    path('', views.index, name = 'portal_index'),
    path('register', views.register, name = 'register')   
>>>>>>> 22b634deb2160efe835c035679c01b1eeda7786e
]