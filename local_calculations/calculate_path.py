from geopy.distance import great_circle
from heapdict import heapdict

from sys import maxsize


def _compute_distance(lat_a, lon_a, lat_b, lon_b):
    return great_circle((lat_a, lon_a), (lat_b, lon_b))


def compute_distance_mi(lat_a, lon_a, lat_b, lon_b):
    return _compute_distance(lat_a, lon_a, lat_b, lon_b).mi


def _dst_btwn_heu(node_a, node_b):
    return compute_distance_mi(node_a.latitude, node_a.longitude,
                               node_b.latitude, node_b.longitude)


def shortest_path(start_node_id, end_node_id, d_graph, debug=False, astar=True):
    visited_nodes = set()

    parent_nodes = dict()
    parent_nodes[start_node_id] = None

    start_node = d_graph[start_node_id]
    end_node = d_graph[end_node_id]

    node_weights = dict()
    node_weights[start_node_id] = 0

    discovered_nodes = heapdict()
    discovered_nodes[start_node_id] = _dst_btwn_heu(start_node, end_node)

    while len(discovered_nodes) != 0:
        parent_id = discovered_nodes.popitem()[0]
        if parent_id == end_node_id:
            break
        visited_nodes.add(parent_id)

        parent_node = d_graph[parent_id]
        for child_id, dist_btwn in parent_node.adjacent.items():
            if child_id not in d_graph:
                if debug and astar:
                    print("{} not found".format(child_id))
                continue

            if child_id in visited_nodes:
                continue

            score = node_weights[parent_id] + dist_btwn
            if score >= node_weights.get(child_id, maxsize):
                continue

            child_node = d_graph[child_id]
            parent_nodes[child_id] = parent_id
            node_weights[child_id] = score

            if astar:
                score += _dst_btwn_heu(child_node, end_node)
            discovered_nodes[child_id] = score

    if debug:
        print("Iterated over {} nodes".format(len(visited_nodes)))

    node_list = []
    current_node_id = end_node_id
    while current_node_id is not None:
        node_list.insert(0, current_node_id)
        current_node_id = parent_nodes[current_node_id]

    return node_list


if __name__ == "__main__":
    from internet_operations.fetch_data_from_web import *
    from graph_builder.build_directed_graph import *

    show_djikstra = False

    d_graph = import_directed_graph("../my_bham_map_graph.json")

    lat_a, lon_a = get_lat_and_lon("1552 woodridge pl")
    nearest_node_a = get_nearest_node(lat_a, lon_a, d_graph, debug=True)

    lat_b, lon_b = get_lat_and_lon("amc vestavia")
    nearest_node_b = get_nearest_node(lat_b, lon_b, d_graph, debug=True)

    path = shortest_path(nearest_node_a.id, nearest_node_b.id, d_graph, debug=True)
    distance = 0
    for i in range(1, len(path)):
        node_a = d_graph[path[i - 1]]
        distance += node_a.adjacent[path[i]]

    print("A Star: {:.2f} miles over {} nodes".format(distance, len(path)))
    for nid in path:
        node = d_graph[nid]
        print(node.ways)

    if show_djikstra:
        path = shortest_path(nearest_node_a.id, nearest_node_b.id, d_graph, debug=True, astar=False)
        distance = 0
        for i in range(1, len(path)):
            node_a = d_graph[path[i - 1]]
            distance += node_a.adjacent[path[i]]

        print("Djikstra: {:.2f} miles over {} nodes".format(distance, len(path)))

    map_b64 = build_gmap_path_image((lat_a, lon_a), (lat_b, lon_b), path, d_graph, debug=True)
    print(map_b64)
