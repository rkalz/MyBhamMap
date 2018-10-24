class Node:
    def __init__(self, id, lat, lon):
        self.id = id
        self.latitude = lat
        self.longitude = lon
        self.adjacent = []
        self.tags = dict()

    def add_tag(self, key, value):
        self.tags[key] = value

    def add_adjacent(self, node_id, distance):
        self.adjacent.append((node_id, distance))