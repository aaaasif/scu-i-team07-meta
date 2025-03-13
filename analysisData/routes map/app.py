import folium
from folium.plugins import MarkerCluster
import pandas as pd
from geopy.distance import great_circle
from math import atan2, radians, degrees, sin, cos
import numpy as np

def calculate_bearing(start, end):
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
        coords.append((interpolated_point.latitude, interpolated_point.longitude))
    return coords

def bezier_curve(start, control, end, num_points=20):
    return [
        (
            (1 - t) ** 2 * start[0] + 2 * (1 - t) * t * control[0] + t ** 2 * end[0],
            (1 - t) ** 2 * start[1] + 2 * (1 - t) * t * control[1] + t ** 2 * end[1],
        )
        for t in np.linspace(0, 1, num_points)
    ]

def generate_color_gradient(num_colors):
    return [
        f"#{int(173 - (i / num_colors) * 173):02x}{int(216 - (i / num_colors) * 216):02x}{int(230 - (i / num_colors) * 230):02x}"
        for i in range(num_colors)
    ]

airport_locations = {
    "LAX": (33.9416, -118.4085), "LGA": (40.7769, -73.8740), "BOS": (42.3656, -71.0096),
    "ATL": (33.6407, -84.4277), "CLT": (35.2140, -80.9431), "JFK": (40.6413, -73.7781), "EWR": (40.6895, -74.1745),
    "MIA": (25.7933, -80.2906), "SFO": (37.6213, -122.3790), "ORD": (41.9742, -87.9073),
    "DEN": (39.8617, -104.6731), "DFW": (32.8998, -97.0403), "DTW": (42.2124, -83.3534), "OAK": (37.6213, -122.3790)
}

routes = [
    ("LGA", "LAX", 9207), ("LAX", "LGA", 9028), ("ATL", "LAX", 8250), ("LAX", "ATL", 8720),
    ("BOS", "LAX", 8243), ("LAX", "BOS", 8695), ("LAX", "JFK", 8131), ("JFK", "LAX", 7876),
    ("LAX", "EWR", 8466), ("CLT", "LAX", 7883)
]

df_routes = pd.DataFrame(routes, columns=["start", "end", "count"])

flight_map = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

airport_cluster = MarkerCluster().add_to(flight_map)
for airport, (lat, lon) in airport_locations.items():
    folium.Marker(
        location=(lat, lon), tooltip=airport,
        icon=folium.Icon(color="blue", icon="plane", prefix="fa")
    ).add_to(airport_cluster)

route_colors = generate_color_gradient(len(routes))

excluded_airports = {"EWR", "MIA", "SFO", "ORD", "DEN", "DFW", "DTW", "OAK"}

airport_layers = {
    airport: folium.FeatureGroup(name=f"Routes from {airport}", show=False).add_to(flight_map)
    for airport in airport_locations if airport not in excluded_airports
}

control_points = {
    ("LAX", "EWR"): (25.0, -100.0), ("LAX", "LGA"): (30.0, -90.0),
    ("JFK", "LAX"): (30.0, -105.0), ("LAX", "BOS"): (32.0, -85.0),
    ("ATL", "LAX"): (26.0, -105.0)
}

for i, (start, end, count) in enumerate(routes):
    if start not in airport_locations or end not in airport_locations:
        continue

    start_coords, end_coords = airport_locations[start], airport_locations[end]

    if (start, end) in control_points or (end, start) in control_points:
        control = control_points.get((start, end), control_points.get((end, start)))
        curved_path = bezier_curve(start_coords, control, end_coords)
    else:
        curved_path = great_circle_path(start_coords, end_coords)

    route_color = route_colors[i]
    route_tooltip = f"{start} → {end}: {count} flights"
    folium.PolyLine(curved_path, color=route_color, weight=4, opacity=0.7, tooltip=route_tooltip).add_to(
        airport_layers.get(start, flight_map)
    )

    mid_index = len(curved_path) // 2
    plane_location = curved_path[mid_index]
    icon_file = "plane.png" if end == "LAX" else "plane2.png"
    folium.Marker(
        location=plane_location, icon=folium.CustomIcon(icon_image=icon_file, icon_size=(70, 70)),
        tooltip=route_tooltip
    ).add_to(airport_layers.get(start, flight_map))

folium.LayerControl(collapsed=False).add_to(flight_map)
flight_map.save("routes.html")
print("Map saved as routes.html.")
