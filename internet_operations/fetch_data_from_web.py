from local_calculations.calculate_path import compute_distance_mi

from geopy.geocoders import GoogleV3
from overpy import Overpass
from motionless import DecoratedMap, LatLonMarker
import requests

from base64 import b64encode
from os import environ
import ssl
from sys import platform


def build_gmap_path_image(start_coords, end_coords, path_ids, graph, debug=False):
    dec_map = DecoratedMap(key=environ["GOOGLE_API_KEY"])
    dec_map.size_x = dec_map.size_y = 640
    dec_map.add_marker(LatLonMarker(start_coords[0], start_coords[1], label="A"))
    dec_map.add_marker(LatLonMarker(end_coords[0], end_coords[1], label="B"))

    for node_id in path_ids:
        path_node = graph[node_id]
        dec_map.add_path_latlon(path_node.latitude, path_node.longitude)

    path_url = dec_map.generate_url()
    if debug:
        print(path_url)

    req = requests.get(path_url)
    return b64encode(req.content).decode()


def get_lat_and_lon(address):
    # Needed for Mac
    ctx = ssl.create_default_context()
    if platform == "darwin":
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

    geolocator = GoogleV3(api_key=environ["GOOGLE_API_KEY"], ssl_context=ctx)
    location_data = geolocator.geocode(address)
    if location_data is None:
        return None

    return location_data.latitude, location_data.longitude


def get_nearest_node(lat, lon, nodes, radius=300, debug=False):
    # 300 meters is roughly 1000 feet
    overpass_api = Overpass()
    query = "node(around:{},{},{});out;".format(radius, lat, lon)
    query_result = overpass_api.query(query)

    closest_node = None
    closest_node_distance = 0
    for node in query_result.nodes:
        if node.id in nodes:
            dist = compute_distance_mi(lat, lon, node.lat, node.lon)
            if closest_node is None or (dist < closest_node_distance and node.id in nodes):
                closest_node = nodes[node.id]
                closest_node_distance = dist

    if closest_node is None:
        return None

    closest_node_distance *= 5280
    if debug:
        print("Nearest node to {:.4f}, {:.4f} is at {:.4f}, {:.4f} and is {:.2f} feet away".format(
            lat, lon, closest_node.latitude, closest_node.longitude, closest_node_distance))

    return closest_node


if __name__ == "__main__":
    from graph_builder.build_directed_graph import import_directed_graph
    d_graph = import_directed_graph("../my_bham_map_graph.json")

    lat_a, lon_a = get_lat_and_lon("1300 University Blvd, Birmingham, AL")
    nearest_node_a = get_nearest_node(lat_a, lon_a, d_graph, debug=True)

    lat_b, lon_b = get_lat_and_lon("100 Ben Chapman Dr, Hoover, AL")
    nearest_node_b = get_nearest_node(lat_b, lon_b, d_graph, debug=True)