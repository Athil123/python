import phonenumbers
from phonenumbers import carrier
from phonenumbers import geocoder
from opencage.geocoder import OpenCageGeocode
import folium
number=input("Enter a valid phone number")
my_number=phonenumbers.parse(number)
number_location=geocoder.description_for_number(my_number,'en')
print(number_location)

api_key='48fec0596989461d842db8e343ce7532'
geocoder=OpenCageGeocode(api_key)

query=str(number_location)
result=geocoder.geocode(query)
print(result)

lat=result[0]['geometry']['lat']
lng=result[0]['geometry']['lng']
print(lat,lng)

my_map=folium.Map(location=[lat,lng],zoom_start=4)
folium.Marker([lat,lng],popup=number_location).add_to((my_map))
my_map.save('my_location.html')