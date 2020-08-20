"""from geopy.distance import geodesic
kolkata = (22.5726, 88.3639) 
delhi = (28.7041, 77.1025)
print(int(geodesic(kolkata, delhi).km))"""

"""import googlemaps 
  
# Requires API key 
gmaps = googlemaps.Client(key='Your_API_key') 
  
# Requires cities name 
my_dist = gmaps.distance_matrix('Delhi','Mumbai')['rows'][0]['elements'][0] 
  
# Printing the result 
print(my_dist) """


from geopy.distance import geodesic
from geopy.geocoders import Nominatim
locator = Nominatim(user_agent = "myGeocoder")

place1 = str(input("enter location 1 - "))
# place2 = str(input("enter location 2 - "))

location1 = locator.geocode(place1)
# location2 = locator.geocode(place2)
i1 = (location1.latitude, location1.longitude)
# i2 = (location2.latitude, location2.longitude)

print('coordinates - ', location1.latitude, ' and ', location1.longitude)
print('address - ', location1.address)

print("distance between them(int km) :- ", int(geodesic(i1, i2).km))
#print(location.longitude, ' - ', location.latitude)