from compute.calculate_data import compute_distance_mi

from geopy.geocoders import GoogleV3
from overpy import Overpass

from os import environ
from sys import platform
import ssl


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
            if closest_node is None or dist < closest_node_distance:
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
    from builder.build_directed_graph import import_directed_graph
    d_graph = import_directed_graph("../my_bham_map_graph.json")

    lat_a, lon_a = get_lat_and_lon("1300 University Blvd, Birmingham, AL")
    nearest_node_a = get_nearest_node(lat_a, lon_a, d_graph, debug=True)

    lat_b, lon_b = get_lat_and_lon("100 Ben Chapman Dr, Hoover, AL")
    nearest_node_b = get_nearest_node(lat_b, lon_b, d_graph, debug=True)