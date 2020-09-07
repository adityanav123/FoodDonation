from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Messages, Locations
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages




## TRYING WHATSAPP MESSAGE
# import os
# from twilio.rest import Client
# auth_token = '33a3dfa60c52cc7e52f0877421c59343'
# account_sid = 'ACe5c1b1ebc45b9158edbe05e5f173bbfe'
# client = Client(account_sid,auth_token)


## JUST TRYING 
import geocoder
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
locator = Nominatim(user_agent = "myGeocoder")


API_KEY = 'pk.eyJ1IjoiYWRpdHlhbmF2IiwiYSI6ImNrZHZwaDB1aTBrOHoycm9ncXM4emI5dGoifQ.oU1UMusmpEUYOS8BMOwo1Q'


DEFAULT_FROM_EMAIL = 'food.donation841@gmail.com'
##


## FAST 2 SMS API USE 
# import requests, json

# def send_sms(number, message):
# 	url = 'https://www.fast2sms.com/dev/bulk'
# 	params = {
# 		'authorization' : '9inWm8qQp6Os12DgwxrR4yZkhajoVNYbtF50BLMdcATKGEfeXPotOgyPHXnA7vE2frUMscT13iNe8IRh',
# 		'sender_id' : 'FSTSMS',
# 		'message' : message,
# 		'numbers' : number,
# 		'route' : 'p'
# 	}
# 	requests.get(url, params = params)




## SIGN UP VIEW FOR THE SIGN UP PAGE.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm # CUSTOM FORM CREATED FOR THE EXTRA FIELDS.
    success_url = reverse_lazy('login') # reverse_lazy finds the url for the 'login' page. ["login" is a keyword that is automatically recognised by django.]
    template_name = 'signup.html'


@login_required(login_url="/users/login") # ITS JUST LIKE AN IF STATEMENT, i.e. only users which are logged in can use this function , no one else/
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

#@login_required(login_url="/users/login")
def pass_change(request):
	#return HttpResponse("<h2> <kbd> password change page - under constuction.</kbd></h2> <br>")
	return render(request, 'password_reset.html')


@login_required(login_url = "/users/login")
def show_nearby_donors(request):
	you = request.user
	you_address = you.locality + ',' + you.city
	#your_location = locator.geocode(you_address)
	donors = CustomUser.objects.filter(city = you.city)
	return render(request, 'show_donors.html', {'you' : you, 'donors' : donors})



## HOME PAGE.. 
def main_page(request): ## TEMPORARY FIX
	#message = Messages.objects.filter(reciever = request.user, read_unread = False).count()
	return render(request, 'home.html')


@login_required(login_url="/users/login")
def updateResources(request,emailid): # WHEN A REQUEST IS MADE BY THE RECIEVER, IT REDIRECTS HERE, to UPDATE THE RECIVER AND THE DONOR TO WHICH REQUEST IS MADE, THE NOTIFICATION LOGIC WOULD BE PRESENT HERE> JUST BEFORE REDIRECTING IT BACK TO THE PAGE.
	you = request.user
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
	return redirect("showNearbyDonors")
	#+14155238886

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
	#coordinates = locator.geocode(address, timeout = 1000)
	g = geocoder.mapbox(address, key=API_KEY)
	lati,lang,users = [], [], []
	near = CustomUser.objects.filter(city = user.city, donor = False)
	merge = ""
	if user.donor == True:
		ans = CustomUser.objects.filter(city = user.city, donor = False)
		for i in ans:
			temp_address = str(i.locality + ', ' + i.city + ', ' + str(i.pin_code) + ', ' + i.state)
			#coord = locator.geocode(temp_address, timeout = 1000)
			g1 = geocoder.mapbox(temp_address, key=API_KEY)
			lati.append(g1.lat)
			lang.append(g1.lng)
			users.append(i)
	return render(request, 'maps.html', {'longitude' : g.lng, 'latitude' : g.lat,  'lat': lati, 'lang': lang, 'users': users, 'near' : near})




@login_required(login_url = "/users/login")
def show_nearby_recievers(request):
	you = request.user
	you_address = you.locality + ',' + you.city
	#your_location = locator.geocode(you_address)
	donors = CustomUser.objects.filter(city = you.city)
	return render(request, 'show_recievers.html', {'you' : you, 'donors' : donors})

@login_required(login_url = "/users/login")
def donation_done(request, pk):
	you = request.user
	them = CustomUser.objects.get(pk = pk)
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
		message = "Donation!! - for " + str(donationOf) + ' people'
		sendRequest = Messages(sender = you, reciever = them, message = message)
		sendRequest.save()
		# SENDING EMAIL ALSO, for notification.
		send_mail(subject = 'Donation!',from_email = 'FoodDonation<food.donation841@gmail.com>' ,message = message + '    Check your account!', recipient_list = [them.email], fail_silently = False)
	them.save()
	you.save()
	return redirect('showNearbyRecievers')


@login_required(login_url = "/users/login")
def check_location(request):
	you = request.user
	admin = CustomUser.objects.get(username = 'admin')
	location = str(you.locality + ', ' + you.city + ', ' + str(you.pin_code) + ', ' + you.state)
	#coordinates = locator.geocode(location, timeout = 1000)
	g = geocoder.mapbox(location, key=API_KEY)

	if g.lat == None:
		message = 'please update your location!'
	else:
		calculate_coordinates(you, location)
		message = 'location found on map.'
	msg = Messages(sender = admin, reciever = you, message = message)
	msg.save()
	return redirect('notification')


# def login_view(request):

# 	if request.method == "POST":
# 		form = AuthenticationForm(request = request, data = request.POST)
# 		if form.is_valid():
# 			username = form.cleaned_data.get('username')
# 			password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#             	login(request, user)
#                 messages.info(request, f"You are now logged in as {username}")
#                 return redirect('homePage')
#             else:
#                 messages.error(request, "Invalid username or password.")
#         else:
#             messages.error(request, "Invalid username or password.")
#     form = AuthenticationForm()
#     return render(request = request,
#                     template_name = "test.html",
#                     context={"form":form})


# def login_view(request):
# 	if request.method == "POST":
# 		form = AuthenticationForm(request = request, data = request.POST)
# 		if form.is_valid():
# 			username = form.cleaned_data.get('username')
# 			password = form.cleaned_data.get('password')
# 			user = authenticate(username = username, password = password)
# 			if user is not None:
# 				login(request, user)
# 				messages.info(request, f'You are now logged in as {username}')

# 				return redirect('homePage')
# 			else:
# 				messages.error(request, 'invalid username/password!')
# 		else:
# 			messages.error(request, 'invalid username/password!')
# 	form = AuthenticationForm()
# 	return render(request, 'home_gc.html', {'form' : form}) 


# def logout_request(request):
#     logout(request)
#     messages.info(request, "Logged out successfully!")
#     return redirect("login_view")

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

		


 