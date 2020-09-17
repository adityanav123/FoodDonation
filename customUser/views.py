from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm, ContactUsForm, AnonymusUserForm
from .models import CustomUser, Messages, Locations
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


## JUST TRYING 
import geocoder
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
locator = Nominatim(user_agent = "myGeocoder")


API_KEY = 'pk.eyJ1IjoiYWRpdHlhbmF2IiwiYSI6ImNrZHZwaDB1aTBrOHoycm9ncXM4emI5dGoifQ.oU1UMusmpEUYOS8BMOwo1Q'


DEFAULT_FROM_EMAIL = 'food.donation841@gmail.com'


## SIGN UP VIEW FOR THE SIGN UP PAGE.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm 
    success_url = reverse_lazy('login') 
    template_name = 'signup.html'


@login_required(login_url="/users/login")
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

def pass_change(request):
	return render(request, 'password_reset.html')


@login_required(login_url = "/users/login")
def show_nearby_donors(request):
	you = request.user
	you_address = you.locality + ',' + you.city
	donors = CustomUser.objects.filter(city = you.city)
	return render(request, 'show_donors.html', {'you' : you, 'donors' : donors})

## HOME PAGE.. 
def main_page(request): 
	return render(request, 'home.html')

@login_required(login_url="/users/login")
def updateResources(request,emailid):
	you = request.user
	if you.resources == 0:
		return redirect('maps')
	req = 0
	them = CustomUser.objects.get(email = emailid)
	if them.resources < you.resources:
		you.resources -= them.resources
		req = them.resources
		them.resources = 0
	else:
		them.resources-=you.resources
		req = you.resources
		you.resources = 0

	# HERE WE SHOULD SEND MESSAGE TO THE SENDER ABOUT THE REQUEST.
	if req > 0:
		message = 'Requested resources for ' + str(req) + ' people.'
		sendRequest = Messages(sender = you, reciever = them, message = message)
		send_mail(subject = 'Donation Request!',from_email = 'FoodDonation<food.donation841@gmail.com>' ,message = message + '   Check your account!', recipient_list = [them.email], fail_silently = False)
		sendRequest.save()
	#SEE ASSUMPTIONS IN README.MD!
	them.save()
	you.save()
	return redirect("maps")

@login_required(login_url = '/users/login')
def seeNotifications(request):
	message = Messages.objects.filter(reciever = request.user)
	context = { 'messages' : message }
	return render(request, 'notification.html', context)

@login_required(login_url = '/users/login')
def deleteNotification(request, pk):
	message = Messages.objects.get(pk = pk)
	message.delete()
	return redirect('notification')

@login_required(login_url = '/users/login')
def readMessage(request, pk):
	message = Messages.objects.get(pk = pk)
	message.read_unread = True
	message.save()
	return redirect('notification')


@login_required(login_url = '/users/login')
def createMap(request):
	user = request.user
	address = str(user.locality + ', ' + user.city + ', ' + str(user.pin_code) + ', ' + user.state)
	g = geocoder.mapbox(address, key=API_KEY)
	lati,lang,users = [], [], []
	near = CustomUser.objects.filter(city = user.city, donor = False)
	merge = ""
	if user.donor == True:
		ans = CustomUser.objects.filter(city = user.city, donor = False)
	else:
		ans = CustomUser.objects.filter(city = user.city, donor = True)
	for i in ans:
		if i.resources > 0:
			temp_address = str(i.locality + ', ' + i.city + ', ' + str(i.pin_code) + ', ' + i.state)
			g1 = geocoder.mapbox(temp_address, key=API_KEY)
			lati.append(g1.lat)
			lang.append(g1.lng)
			users.append(i)
	return render(request, 'maps.html', {'longitude' : g.lng, 'latitude' : g.lat,  'lat': lati, 'lang': lang, 'users': users, 'near' : near})


@login_required(login_url = "/users/login")
def show_nearby_recievers(request):
	you = request.user
	you_address = you.locality + ',' + you.city
	donors = CustomUser.objects.filter(city = you.city)
	return render(request, 'show_recievers.html', {'you' : you, 'donors' : donors})

@login_required(login_url = "/users/login")
def donation_done(request, email):
	you = request.user
	if you.resources == 0:
		return redirect('maps')
	them = CustomUser.objects.get(email = email)
	donationOf = 0 # resources donated.
	if them.resources >= you.resources:
		donationOf = them.resources
		them.resources -= you.resources
		you.resources = 0
	else:
		donationOf = them.resources
		you.resources -= them.resources
		them.resources = 0
	if donationOf > 0:
		message = "Donation for " + str(donationOf) + ' people'
		sendRequest = Messages(sender = you, reciever = them, message = message)
		sendRequest.save()
		# SENDING EMAIL ALSO, for notification.
		send_mail(subject = 'Donation!',from_email = 'FoodDonation<food.donation841@gmail.com>' ,message = message + '    Check your account!', recipient_list = [them.email], fail_silently = False)
	them.save()
	you.save()
	return redirect('maps')


def calculate_coordinates(user, address): # TO STORE THE ADDRESS IN THE DATABASE.
	g = geocoder.mapbox(address, key = API_KEY)
	try:
		if_present = Locations.objects.get(user_id = user)	
	except Locations.DoesNotExist:
		add_location = Locations(user_id = user, latitude = g.lat, longitude = g.lng)
		add_location.save()
		return
	if_present.latitude = g.lat
	if_present.longitude = g.lng
	if_present.save()


def ContactUs(request):
	if request.method == "POST":
		form = ContactUsForm(request.POST)
		if form.is_valid():
			message = form.cleaned_data.get('message')
			email = form.cleaned_data.get('email')
			message = 'From - ' + email + '\n' + message
			send_mail(subject = 'Someone Contacted!',from_email = 'FoodDonation<food.donation841@gmail.com>' ,message = message , recipient_list = ['food.donation841@gmail.com'], fail_silently = False)
			return redirect('homePage')
	else:
		form = ContactUsForm()
		return render(request, 'contact_us.html', { 'form' : form })


def AnonymusUserRequest(request):
	if request.method == "POST":
		form = AnonymusUserForm(request.POST)
		if form.is_valid():
			message = form.cleaned_data.get('message')
			email = form.cleaned_data.get('email')
			name = form.cleaned_data.get( 'name')
			resources = form.cleaned_data.get('resources')
			message = '' + message + '\nRequest/Donation for - ' + str(resources) + ' people.\nContact the person.\nEmail : ' + email + '\nName : ' + name
			send_mail(subject = 'Anonymus User Request/Donation',  from_email = 'AnonymusUser<food.donation841@gmail.com>', message = message, recipient_list = ['support_fooddonation@protonmail.com'] , fail_silently = False)
			return redirect('home')
	else:
		form = AnonymusUserForm()
		return render(request, 'anonymusUser.html', {'form' : form })
