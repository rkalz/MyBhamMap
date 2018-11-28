from builder.parse_osm_xml import *

from fetcher.fetch_data import compute_distance_mi

import pickle


def build_directed_graph(nodes, ways):
    for way in ways:
        for i in range(1, len(way.nodes)):
            node_a = nodes[way.nodes[i-1]]
            node_b = nodes[way.nodes[i]]

            node_a.ways.add(way.name)
            node_b.ways.add(way.name)

            # Compute distance between nodes, define a -> b
            distance = compute_distance_mi(node_a.latitude, node_a.longitude,
                                           node_b.latitude, node_b.longitude)
            node_a.add_adjacent(node_b.id, distance)
            if not way.is_one_way:
                # If it's not one way, also define b -> a
                node_b.add_adjacent(node_a.id, distance)

    directed_graph = dict()
    for node in nodes.values():
        # Build new dict containing only nodes with connections
        if len(node.adjacent) != 0:
            directed_graph[node.id] = node

    return directed_graph


def export_directed_graph(d_graph, file_name):
    with open(file_name, "wb") as f:
        f.write(pickle.dumps(d_graph))


def import_directed_graph(file_name):
    with open(file_name, "rb") as f:
        d_graph = pickle.loads(f.read())
    return d_graph


if __name__ == "__main__":
    roads, nodes = parse_osm_file("../osm_birmingham.xml")
    directed_graph = build_directed_graph(nodes, roads)

    export_directed_graph(directed_graph, "../my_bham_map_graph.pickle")