import folium
import pandas as pd
from geopy.distance import great_circle
from math import atan2, radians, degrees, sin, cos
import numpy as np

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
    """Generate a Bézier curve between two points."""
    return [
        (
            (1 - t) ** 2 * start[0] + 2 * (1 - t) * t * control[0] + t ** 2 * end[0],
            (1 - t) ** 2 * start[1] + 2 * (1 - t) * t * control[1] + t ** 2 * end[1],
        )
        for t in np.linspace(0, 1, num_points)
    ]

airport_locations = {
    "LAX": (33.9416, -118.4085), "LGA": (40.7769, -73.8740), "BOS": (42.3656, -71.0096),
    "ATL": (33.6407, -84.4277), "CLT": (35.2140, -80.9431), "JFK": (40.6413, -73.7781), "EWR": (40.6895, -74.1745)
}

routes = [
    ("LGA", "LAX", 9207), ("LAX", "LGA", 9028), ("LAX", "ATL", 8720), ("ATL", "LAX", 8250),
    ("LAX", "BOS", 8695), ("BOS", "LAX", 8243), ("LAX", "JFK", 8131), ("JFK", "LAX", 7876),
    ("LAX", "EWR", 8466), ("CLT", "LAX", 7883)
]

df_routes = pd.DataFrame(routes, columns=["start", "end", "count"])

flight_map = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

def generate_color_gradient(num_colors):
    """Generate a color gradient for route visualization."""
    return [f"#{int(173 - (i / num_colors) * 173):02x}{int(216 - (i / num_colors) * 216):02x}{int(230 - (i / num_colors) * 230):02x}" for i in range(num_colors)]

route_colors = generate_color_gradient(len(routes))

airport_layers = {
    airport: folium.FeatureGroup(name=f"Routes from {airport}", show=False).add_to(flight_map)
    for airport in airport_locations
}

for airport, (lat, lon) in airport_locations.items():
    folium.Marker(location=(lat, lon), tooltip=airport, icon=folium.Icon(color="blue", icon="plane", prefix="fa")).add_to(flight_map)

for i, (start, end, count) in enumerate(routes):
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
    folium.PolyLine(curved_path, color=route_color, weight=4, opacity=0.7, tooltip=f"{start} → {end}: {count} flights").add_to(airport_layers[start])
    
    mid_index = len(curved_path) // 2
    plane_location = curved_path[mid_index]
    icon_file = "plane.png" if end == "LAX" else "plane2.png"
    folium.Marker(location=plane_location, icon=folium.CustomIcon(icon_image=icon_file, icon_size=(70, 70)), tooltip=f"{start} → {end}: {count} flights").add_to(airport_layers[start])

folium.LayerControl(collapsed=False).add_to(flight_map)
flight_map.save("flight_routes_map.html")
print("Map saved as flight_routes_map.html.")
