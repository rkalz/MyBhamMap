from builder.parse_osm_xml import *

from math import atan2, cos, pi, sin, sqrt


def _degrees_to_radians(degree):
    return degree * pi / 180.0


def _distance_btwn_points_in_mi(lat_a, lon_a, lat_b, lon_b):
    # Taken from https://www.movable-type.co.uk/scripts/latlong.html

    phi_1 = _degrees_to_radians(lat_a)
    phi_2 = _degrees_to_radians(lat_b)
    delta_phi = _degrees_to_radians(lat_b - lat_a)
    delta_lambda = _degrees_to_radians(lon_b - lon_a)

    # In miles
    RADIUS_OF_EARTH = 6371 / 1.609

    a = sin(delta_phi/2) * sin(delta_phi/2) + cos(phi_1) * cos(phi_2) * \
        sin(delta_lambda/2) * sin(delta_lambda/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return RADIUS_OF_EARTH * c


def build_directed_graph(nodes, ways):
    for way in ways:
        for i in range(1, len(way.nodes)):
            node_a = nodes[way.nodes[i-1]]
            node_b = nodes[way.nodes[i]]

            # Compute distance between nodes, set define a -> b
            distance = _distance_btwn_points_in_mi(node_a.latitude, node_a.longitude, node_b.latitude, node_b.longitude)
            node_a.add_adjacent(node_b, distance)
            if not way.is_one_way:
                # If it's not one way, also defined b -> a
                node_b.add_adjacent(node_a, distance)

    directed_graph = dict()

    for node in nodes.values():
        # Build new dict containing only nodes with connections
        if len(node.adjacent) != 0:
            directed_graph[node.id] = node

    return directed_graph


if __name__ == "__main__":
    roads, nodes = parse_osm_file("../osm_birmingham.xml")
    directed_graph = build_directed_graph(nodes, roads)
    print("Out of", str(len(nodes)), "nodes,", str(len(directed_graph)), "were added to the directed graph")