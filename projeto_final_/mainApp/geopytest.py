from geopy.geocoders import MapBox
api_key = "pk.eyJ1IjoidW5paG91c2VzIiwiYSI6ImNrbGltdHJxcDBlZWEyd25tYmtkc2xuNmIifQ.hX3RupN9qPRjEJ9oHAFMQg"
geolocator = MapBox(api_key, scheme=None,  user_agent=None, domain='api.mapbox.com')
                    
location = geolocator.geocode("Rua das Janelas verdes")

print(location.latitude, location.longitude)