from math import atan2, pi


def _angle_of_three(node_a, node_b, node_c):
    p2_x = node_a.latitude * pi / 180.0
    p2_y = node_a.longitude * pi / 180.0
    p1_x = node_b.latitude * pi / 180.0
    p1_y = node_b.longitude * pi / 180.0
    p3_x = node_c.latitude * pi / 180.0
    p3_y = node_c.longitude * pi / 180.0

    ang_rad = atan2(p2_y - p1_y, p2_x - p1_x) - \
              atan2(p3_y - p1_y, p3_x - p1_x)

    ang_deg = ang_rad * 180.0 / pi
    if ang_deg < 0:
        ang_deg += 360

    return ang_deg


def build_direction_list(nodes, d_graph):
    d_list = []

    for i in range(1, len(nodes)-1):
        a = d_graph[nodes[i - 1]]
        b = d_graph[nodes[i]]
        c = d_graph[nodes[i + 1]]
        angle = _angle_of_three(a, b, c)

    return d_list


if __name__ == "__main__":
    from fetcher.fetch_data import *
    from builder.build_directed_graph import *
    from compute.calculate_data import shortest_path

    d_graph = import_directed_graph("../my_bham_map_graph.json")

    lat_a, lon_a = get_lat_and_lon("UAB BEC")
    nearest_node_a = get_nearest_node(lat_a, lon_a, d_graph)

    lat_b, lon_b = get_lat_and_lon("Hoover Met")
    nearest_node_b = get_nearest_node(lat_b, lon_b, d_graph)

    path = shortest_path(nearest_node_a.id, nearest_node_b.id, d_graph)
    build_direction_list(path, d_graph)