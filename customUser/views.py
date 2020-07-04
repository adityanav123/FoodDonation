from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


## JUST TRYING 
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
locator = Nominatim(user_agent = "myGeocoder")

##


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


@login_required(login_url="{% url 'login'%}")
def edit_profile(request):
	if request.method == "POST":
		form = CustomUserChangeForm(request.POST, instance = request.user)
		if form.is_valid():
			form.save()
			return redirect('home')
		else:
			return HttpResponse('something is not right! (look again at the code)')
	elif request.method == "GET":
		form = CustomUserChangeForm(instance = request.user)
		context = {'form' : form }
		return render(request, 'edit_form.html', context)


@login_required(login_url="{% url 'login'%}")
def pass_change(request):
	#return HttpResponse("<h2> <kbd> password change page - under constuction.</kbd></h2> <br>")
	return render(request, 'pass_change.html')



def show_nearby_donors(request):
	you = request.user
	you_address = you.locality + ',' + you.city
	#your_location = locator.geocode(you_address)
	donors = CustomUser.objects.filter(city = you.city)
	return render(request, 'show_donors.html', {'you' : you, 'donors' : donors})


def main_page(request): ## TEMPORARY FIX
	return render(request, 'home.html')




 