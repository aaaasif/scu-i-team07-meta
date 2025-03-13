import folium
from folium.plugins import MarkerCluster 
import pandas as pd
from geopy.distance import great_circle
from math import atan2, radians, degrees, sin, cos
import numpy as np
import csv

routes = []

with open("routes.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  
    for row in reader:
        start = row[0] 
        end = row[1]  
        fare = float(row[2]) 
        airline = row[3]  
        routes.append([start, end, fare, airline]) 

def calculate_bearing(start, end):
    """Calculate the bearing between two geographic points."""
    lat1, lon1 = map(radians, start)
    lat2, lon2 = map(radians, end)
    delta_lon = lon2 - lon1
    
    x = atan2(
        sin(delta_lon) * cos(lat2),
        cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(delta_lon)
    )
    return (degrees(x) + 360) % 360 

def great_circle_path(start, end, num_points=20):
    coords = []
    for i in range(num_points + 1):
        fraction = i / num_points
        interpolated_point = great_circle(fraction * great_circle(start, end).km).destination(start, calculate_bearing(start, end))
        coords.append((interpolated_point.latitude, interpolated_point.longitude))  # Convert Point to Tuple
    return coords


def bezier_curve(start, control, end, num_points=30):
    return [
        (
            (1 - t) ** 2 * start[0] + 2 * (1 - t) * t * control[0] + t ** 2 * end[0],
            (1 - t) ** 2 * start[1] + 2 * (1 - t) * t * control[1] + t ** 2 * end[1],
        )
        for t in np.linspace(0, 1, num_points)
    ]

airport_locations = {
    "LAX": (33.9416, -118.4085), "LGA": (40.7769, -73.8740), "BOS": (42.3656, -71.0096),
    "ATL": (33.6407, -84.4277), "CLT": (35.2140, -80.9431), "JFK": (40.6413, -73.7781), "EWR": (40.6895, -74.1745),
    "MIA": (25.7933, -80.2906), "SFO": (37.6213, -122.3790), "ORD": (41.9742, -87.9073),
    "DEN": (39.8617, -104.6731), "DFW": (32.8998, -97.0403), "DTW": (42.2124, -83.3534), "OAK": (37.6213, -122.3790)
}

df_routes = pd.DataFrame(routes, columns=["start", "end", "cheapestFare", "cheapestAirline"])

flight_map = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

airport_cluster = MarkerCluster().add_to(flight_map)
for airport, (lat, lon) in airport_locations.items():
    folium.Marker(location=(lat, lon), tooltip=airport, icon=folium.Icon(color="blue", icon="plane", prefix="fa")).add_to(airport_cluster)

def generate_color_gradient(num_colors):
    """Generate a color gradient for route visualization."""
    return [f"#{int(173 - (i / num_colors) * 173):02x}{int(216 - (i / num_colors) * 216):02x}{int(230 - (i / num_colors) * 230):02x}" for i in range(num_colors)]

route_colors = generate_color_gradient(len(routes))

airport_layers = {
    airport: folium.FeatureGroup(name=f"Routes from {airport}", show=False).add_to(flight_map)
    for airport in airport_locations
}

for i, (start, end, fare, airline) in enumerate(routes):
    if start not in airport_locations or end not in airport_locations:
        continue

    start_coords, end_coords = airport_locations[start], airport_locations[end]
    
    control_points = {
        ("LAX", "EWR"): (25.0, -100.0), ("LAX", "LGA"): (30.0, -90.0),
        ("JFK", "LAX"): (30.0, -105.0), ("LAX", "BOS"): (32.0, -85.0),
        ("ATL", "LAX"): (26.0, -105.0)
    }
    
    curved_path = bezier_curve(start_coords, control_points.get((start, end), control_points.get((end, start), None)), end_coords, num_points=30) if (start, end) in control_points or (end, start) in control_points else great_circle_path(start_coords, end_coords, num_points=30)
    
    route_color = route_colors[i]
   
    route_tooltip = f"{start} → {end}: Cheapest Fare: ${fare} | Airline: {airline}"
    folium.PolyLine(curved_path, color=route_color, weight=4, opacity=0.7, tooltip=route_tooltip).add_to(airport_layers[start])

    mid_index = len(curved_path) // 2
    plane_location = curved_path[mid_index]
    icon_file = "plane.png" if end == "LAX" else "plane2.png"
    folium.Marker(location=plane_location, icon=folium.CustomIcon(icon_image=icon_file, icon_size=(70, 70)), tooltip=route_tooltip).add_to(airport_layers[start])

folium.LayerControl(collapsed=False).add_to(flight_map)
flight_map.save("flight_routes_map_with_prices.html")
print("Map saved as flight_routes_map_with_prices.html.")