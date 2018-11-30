import xml.etree.ElementTree as et

from objects.node import Node
from objects.way import Way


def extract_road(item, roads):
    way_id = int(item.attrib['id'])
    way = Way(way_id)
    is_highway = False

    for child in item:
        if child.tag == "nd":
            way.add_node(int(child.attrib['ref']))
        elif child.tag == "tag":
            key = child.attrib['k']
            val = child.attrib['v']
            if key == "name":
                way.name = val
            elif key == "oneway":
                    way.is_one_way = val == "yes"
            elif key == "highway":
                is_highway = True

    if way.name is not None and is_highway:
        roads.append(way)


def extract_node(item, nodes):
    node_id = int(item.attrib['id'])
    node_lat = float(item.attrib['lat'])
    node_lon = float(item.attrib['lon'])
    node = Node(node_id, node_lat, node_lon)
    for child in item:
        key = child.attrib['k']
        val = child.attrib['v']
        if child.tag == "tag":
            node.add_tag(key, val)

    nodes[node_id] = node


def parse_osm_file(filename):
    tree = et.parse(filename)

    roads = []
    nodes = dict()

    for item in tree.iter():
        if item.tag == "node":
            extract_node(item, nodes)
        elif item.tag == "way":
            extract_road(item, roads)

    return roads, nodes


if __name__ == "__main__":
    roads, nodes = parse_osm_file("../osm_birmingham.xml")
    print(str(len(nodes)) + " nodes in dataset")
    print(str(len(roads)) + " roads in dataset")
    pass
