import geocoder
g = geocoder.mapbox('NEB Extension, Alwar', key='pk.eyJ1IjoiYWRpdHlhbmF2IiwiYSI6ImNrZHZwaDB1aTBrOHoycm9ncXM4emI5dGoifQ.oU1UMusmpEUYOS8BMOwo1Q')

#print(g.json)

print('latitude - ', g.lat, '\nlongitude - ', g.lng)