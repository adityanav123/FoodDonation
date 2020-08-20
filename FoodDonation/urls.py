"""FoodDonation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
#from portal import views as portal_view
from django.contrib.auth import views as auth_views # for login logout.
from django.views.generic.base import TemplateView
from customUser import views as user_view

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', TemplateView.as_view(template_name = 'home.html'), name = 'home'),
    path('', user_view.login_view, name = 'home'),
    path('loginView/',user_view.login_view, name = 'login_view'),
    path('logout/',user_view.logout_request, name = 'logout_view'),
    path('users/', include('customUser.urls')),
    path('users/', include('django.contrib.auth.urls')),
    #path('edit_user/', user_view.edit_form, name = 'edit_form'),
    path('main/', user_view.main_page, name = 'homePage'),
]
