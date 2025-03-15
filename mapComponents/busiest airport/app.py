import folium
from folium.plugins import MarkerCluster
import pandas as pd
import numpy as np
from geopy.distance import great_circle
from math import atan2, radians, degrees, sin, cos
import csv
from branca.element import Element

routes = []
with open("routes.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  
    for row in reader:
        start, end, fare, airline = row[0], row[1], float(row[2]), row[3]
        routes.append([start, end, fare, airline])

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

m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

airport_cluster = MarkerCluster().add_to(m)
for airport, (lat, lon) in airport_locations.items():
    folium.Marker(location=(lat, lon), tooltip=airport, icon=folium.Icon(color="blue", icon="plane", prefix="fa")).add_to(airport_cluster)

def generate_color_gradient(num_colors):
    min_r, min_g, min_b = 32, 64, 96  
    return [
        f"#{int(173 - (i / num_colors) * (173 - min_r)):02x}"
        f"{int(216 - (i / num_colors) * (216 - min_g)):02x}"
        f"{int(230 - (i / num_colors) * (230 - min_b)):02x}"
        for i in range(num_colors)
    ]

route_colors = generate_color_gradient(len(routes))
excluded_airports = {"LAX", "LGA", "JFK", "EWR", "MIA", "SFO", "ORD", "OAK"}

airport_layers = {
    airport: folium.FeatureGroup(name=f"Routes from {airport}", show=False).add_to(m)
    for airport in airport_locations if airport not in excluded_airports
}

for i, (start, end, fare, airline) in enumerate(routes):
    if start in excluded_airports and end in excluded_airports:
        continue
    if start not in airport_locations or end not in airport_locations:
        continue
    
    start_coords, end_coords = airport_locations[start], airport_locations[end]
    control_points = {
        ("LAX", "EWR"): (25.0, -100.0), ("LAX", "LGA"): (30.0, -90.0),
        ("JFK", "LAX"): (30.0, -105.0), ("LAX", "BOS"): (32.0, -85.0),
        ("ATL", "LAX"): (26.0, -105.0)
    }
    
    curved_path = bezier_curve(start_coords, control_points.get((start, end), control_points.get((end, start), None)), end_coords, num_points=30) \
        if (start, end) in control_points or (end, start) in control_points else great_circle_path(start_coords, end_coords, num_points=30)
    
    route_color = route_colors[i]
    route_tooltip = f"{start} → {end}: Cheapest Fare: ${fare} | Airline: {airline}"
    folium.PolyLine(curved_path, color=route_color, weight=4, opacity=0.7, tooltip=route_tooltip).add_to(airport_layers[start])
    
    mid_index = len(curved_path) // 2
    plane_location = curved_path[mid_index]
    icon_file = "plane.png" if end == "LAX" else "plane2.png"
    folium.Marker(location=plane_location, icon=folium.CustomIcon(icon_image=icon_file, icon_size=(70, 70)), tooltip=route_tooltip).add_to(airport_layers[start])
    
folium.LayerControl(collapsed=False).add_to(m)

def create_table():
    data = [
        ("LAX", 103645, 101148, 204793), ("LGA", 80752, 80949, 161701), ("BOS", 76455, 71371, 147826),
        ("DFW", 73045, 74562, 147607), ("ORD", 70767, 72157, 142924), ("MIA", 67672, 73220, 140892),
        ("SFO", 71166, 69163, 140329), ("ATL", 68423, 71326, 139749), ("CLT", 68121, 68511, 136632),
        ("DEN", 60115, 63350, 123465)
    ]
    
    row_colors = [
        "#ff6b6b", "#ff7f7f", "#ff9393", "#ffa6a6", "#ffb8b8", "#ffcccc", 
        "#ffd1d1", "#ffe0e0", "#ffe6e6", "#fff2f2"
    ]
    
    table_html = """
<div id="draggable-table" style="position: fixed; bottom: 10px; left: 10px; z-index: 9999; background: white; padding: 10px; 
                border: 1px solid #ddd; border-radius: 8px; font-size: 15px; width: 30%; overflow-x: auto; cursor: move;">
    <b style="font-size: 15px; font-weight: bold;">Airport Flight Data</b>
    <table border="1" style="border-collapse: collapse; width: 100%; font-size: 15px;">
        <thead style="background-color: #f2f2f2;">
            <tr>
                <th style="padding: 6px; text-align: left;">Airport</th>
                <th style="padding: 6px; text-align: center;">Departures</th>
                <th style="padding: 6px; text-align: center;">Arrivals</th>
                <th style="padding: 6px; text-align: center;">Total Flights</th>
            </tr>
        </thead>
        <tbody>
    """
<<<<<<< HEAD
    
=======
>>>>>>> b1b7b2df76ff768e89393a7e14c3bba8be32a497
    for index, (airport, departures, arrivals, total) in enumerate(data):
        row_color = row_colors[index % len(row_colors)]
        
        table_html += f"""
        <tr style="background-color: {row_color}; transition: background-color 0.3s;" 
            onmouseover="this.style.backgroundColor='#f0f0f0';" 
            onmouseout="this.style.backgroundColor='{row_color}';">
            <td style="padding: 6px; text-align: left; font-weight: normal;">{airport}</td>
            <td style="padding: 6px; text-align: center;">{departures}</td>
            <td style="padding: 6px; text-align: center;">{arrivals}</td>
            <td style="padding: 6px; text-align: center;">{total}</td>
        </tr>
        """
    table_html += """
        </tbody>
    </table>
</div>
<script>
    var dragElement = document.getElementById("draggable-table");

    dragElement.onmousedown = function(event) {
        var shiftX = event.clientX - dragElement.getBoundingClientRect().left;
        var shiftY = event.clientY - dragElement.getBoundingClientRect().top;

        dragElement.style.position = 'absolute';
        dragElement.style.zIndex = 1000;
        document.body.append(dragElement);

        moveAt(event);

        function moveAt(e) {
            dragElement.style.left = e.clientX - shiftX + 'px';
            dragElement.style.top = e.clientY - shiftY + 'px';
        }

        document.onmousemove = function(event) {
            moveAt(event);
        };

        dragElement.onmouseup = function() {
            document.onmousemove = null;
            dragElement.onmouseup = null;
        };
    };

    dragElement.ondragstart = function() {
        return false;
    };
</script>
    """
    return table_html

table = Element(create_table())
m.get_root().html.add_child(table)

m.save('m.html')
print("Map with table saved as 'm.html'.")