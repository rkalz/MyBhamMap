from graph_builder.parse_osm_xml import *
from graph_builder.build_directed_graph import *
from internet_operations.fetch_data_from_web import *
from local_calculations.calculate_path import *
from base64 import b64decode
from time import time


if __name__ == "__main__":
    print("Generating graph")
    roads, nodes = parse_osm_file("osm_birmingham.xml")
    d_graph = build_directed_graph(nodes, roads)

    while True:
        try:
            first_pos = input("Enter start location: ")
            second_pos = input("Enter end location: ")

            lat_a, lon_a = get_lat_and_lon(first_pos)
            nearest_node_a = get_nearest_node(lat_a, lon_a, d_graph, debug=False)

            lat_b, lon_b = get_lat_and_lon(second_pos)
            nearest_node_b = get_nearest_node(lat_b, lon_b, d_graph, debug=False)

            path = shortest_path(nearest_node_a.id, nearest_node_b.id, d_graph, debug=True)
            distance = 0
            for i in range(1, len(path)):
                node_a = d_graph[path[i - 1]]
                distance += node_a.adjacent[path[i]]

            print("A Star: {:.2f} miles over {} nodes".format(distance, len(path)))

            path = shortest_path(nearest_node_a.id, nearest_node_b.id, d_graph, debug=True, astar=False)
            distance = 0
            for i in range(1, len(path)):
                node_a = d_graph[path[i - 1]]
                distance += node_a.adjacent[path[i]]

            print("Djikstra: {:.2f} miles over {} nodes".format(distance, len(path)))

            map_b64 = build_gmap_path_image((lat_a, lon_a), (lat_b, lon_b), path, d_graph, debug=False)

            map_bytes = b64decode(map_b64)
            file_name = str(int(time())) + ".png"
            with open("images/" + file_name, "wb") as f:
                f.write(map_bytes)

            print("http://104.196.183.178/" + file_name)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("An error occured: ", str(e))
            continue
