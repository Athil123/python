import gmplot
import googlemaps
from geopy.geocoders import GoogleV3
import polyline

# Replace with your Google Maps API key
google_maps_api_key = "AIzaSyCMSw2jUr2A7jeBbTazwZ3zR0gzPs-yY3U"

# Initialize map
gmap = gmplot.GoogleMapPlotter(0, 0, 10, apikey=google_maps_api_key)

# Initialize starting and destination places
geolocator = GoogleV3(api_key=google_maps_api_key)
start_place = ""
dest_place = ""
start_lat = 0
start_lng = 0
dest_lat = 0
dest_lng = 0

# Initialize the Google Maps client
gmaps = googlemaps.Client(key=google_maps_api_key)

# Create a function to update the bus's position based on the user's current location
def update_bus_position():
    global start_place, dest_place, start_lat, start_lng, dest_lat, dest_lng
    # Determine the user's current location (e.g., using GPS or other location services)
    user_location = input("Enter your current location: ")
    
    # Use geocoding to convert the user's location to coordinates
    location = geolocator.geocode(user_location)
    if location:
        start_place = user_location
        start_lat, start_lng = location.latitude, location.longitude
        # Set the destination as the same place for simplicity
        dest_place = user_location
        dest_lat, dest_lng = start_lat, start_lng

# Create a function to get the path and distance between places
def get_path_and_distance():
    directions = gmaps.directions(start_place, dest_place, mode="driving")
    if directions:
        route = directions[0]["legs"][0]
        distance = route["distance"]["text"]
        polyline_data = directions[0]["overview_polyline"]["points"]
        return distance, polyline_data

# Create a live tracking loop
while True:
    update_bus_position()
    
    # Get the distance and path
    distance, path = get_path_and_distance()
    
    # Clear the previous plot
    gmap.marker(start_lat, start_lng, color='red', title='Bus')
    
    # Decode the polyline and draw the path on the map
    decoded_path = polyline.decode(path)
    lats, lngs = zip(*decoded_path)
    gmap.plot(lats, lngs, 'blue', edge_width=2)
    
    # Add an information marker for the distance
    info_marker_lat = (start_lat + dest_lat) / 2
    info_marker_lng = (start_lng + dest_lng) / 2
    info_text = f"Distance: {distance}"
    gmap.marker(info_marker_lat, info_marker_lng, color='green', title=info_text)
    
    # Save the map to an HTML file (replace 'bus_tracking.html' with your desired file name)
    gmap.draw('bus_tracking.html')

    print("Bus position and route information updated on the map.")
    print(directions)