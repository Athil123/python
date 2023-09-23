import googlemaps
import folium

# Replace with your Google Maps API key
google_maps_api_key = "AIzaSyCMSw2jUr2A7jeBbTazwZ3zR0gzPs-yY3U"

# Initialize the Google Maps client
gmaps = googlemaps.Client(key=google_maps_api_key)

# Create a function to get the path and distance between places
def get_path_and_distance(from_place, to_place):
    directions = gmaps.directions(from_place, to_place, mode="driving")
    if directions:
        route = directions[0]["legs"][0]
        distance = route["distance"]["text"]
        polyline_data = directions[0]["overview_polyline"]["points"]
        return distance, polyline_data

# Ask for "from" and "to" places
from_place = input("Enter the starting place: ")
to_place = input("Enter the destination place: ")

# Get the distance and path
distance, path = get_path_and_distance(from_place, to_place)

# Decode the polyline and draw the path on the map
decoded_path = googlemaps.convert.decode_polyline(path)
lats, lngs = zip(*decoded_path)

# Ensure that the decoded coordinates are correctly converted to floats
lats = [float(lat) for lat in lats]
lngs = [float(lng) for lng in lngs]

# Calculate the map center
map_center = [(min(lats) + max(lats)) / 2, (min(lngs) + max(lngs)) / 2]

# Create a map centered between the "from" and "to" places
m = folium.Map(location=map_center, zoom_start=10)

# Add markers for "from" and "to" places
folium.Marker(location=[min(lats), min(lngs)], popup="From", icon=folium.Icon(color="red")).add_to(m)
folium.Marker(location=[max(lats), max(lngs)], popup="To", icon=folium.Icon(color="green")).add_to(m)

# Create a path using the decoded coordinates
folium.PolyLine(list(zip(lats, lngs), color="blue", weight=5, opacity=0.7).add_to(m))

# Add a marker for the distance
distance_marker_lat = (min(lats) + max(lats)) / 2
distance_marker_lng = (min(lngs) + max(lngs)) / 2
distance_text = f"Distance: {distance}"
folium.Marker([distance_marker_lat, distance_marker_lng], popup=distance_text, icon=folium.Icon(color="orange")).add_to(m)

# Save the map to an HTML file
m.save('route_map.html')

print(f"Distance between {from_place} and {to_place}: {distance}")
