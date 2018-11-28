from geopy.distance import great_circle
from geopy.geocoders import Nominatim, options
from overpy import Overpass

import ssl


def _compute_distance(lat_a, lon_a, lat_b, lon_b):
    return great_circle((lat_a, lon_a), (lat_b, lon_b))


def compute_distance_mi(lat_a, lon_a, lat_b, lon_b):
    return _compute_distance(lat_a, lon_a, lat_b, lon_b).mi


def get_lat_and_lon(address):
    # Needed for Mac
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    options.default_ssl_context = ctx

    geolocator = Nominatim(user_agent="MyBhamMap 1.0")
    location_data = geolocator.geocode(address)
    if location_data is None:
        return None

    return location_data.latitude, location_data.longitude


def get_nearest_node(lat, lon, nodes, radius=300):
    # 300 meters is roughly 1000 feet
    overpass_api = Overpass()
    query = "node(around:{},{},{});out;".format(str(radius), str(lat), str(lon))
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

    return closest_node


if __name__ == "__main__":
    from builder.build_directed_graph import import_directed_graph
    d_graph = import_directed_graph("../my_bham_map_graph.pickle")
    del import_directed_graph

    lat_a, lon_a = get_lat_and_lon("1300 University Blvd, Birmingham, AL")
    nearest_node_a = get_nearest_node(lat_a, lon_a, d_graph)
    print("{},{}".format(str(nearest_node_a.latitude), str(nearest_node_a.longitude)))

    lat_b, lon_b = get_lat_and_lon("2235 Lime Rock Rd, Vestavia Hills, AL")
    nearest_node_b = get_nearest_node(lat_b, lon_b, d_graph)
    print("{},{}".format(str(nearest_node_b.latitude), str(nearest_node_b.longitude)))