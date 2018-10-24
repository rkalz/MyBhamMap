import xml.etree.ElementTree as et
from objects.node import Node
from objects.way import Way


def parse_osm_file(filename):
    tree = et.parse(filename)
    roads = dict()
    nodes = dict()

    for item in tree.iter():
        if item.tag == "node":
            node_id = int(item.attrib['id'])
            node_lat = float(item.attrib['lat'])
            node_lon = float(item.attrib['lon'])
            node = Node(node_id, node_lat, node_lon)
            for child in item:
                if child.tag == "tag":
                    node.add_tag(child.attrib['k'], child.attrib['v'])
            nodes[node_id] = node

        elif item.tag == "way":
            way_id = int(item.attrib['id'])
            way = Way(way_id)
            for child in item:
                if child.tag == "nd":
                    way.add_node(child.attrib['ref'])
                elif child.tag == "tag":
                    key = child.attrib['k']
                    val = child.attrib['v']
                    if key == "name":
                        way.set_name(val)
                    else:
                        way.add_tag(key, val)
                if way.name is not None and "transmission line" not in way.name.lower():
                    roads[way.name] = way

    return roads, nodes


if __name__ == "__main__":
    roads, nodes = parse_osm_file("osm_birmingham.xml")
    print(str(len(nodes)) + " nodes in dataset")
    print(str(len(roads)) + " roads in dataset")
    pass