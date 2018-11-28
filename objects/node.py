class Node:
    def __init__(self, id, lat, lon):
        self.id = id
        self.latitude = lat
        self.longitude = lon
        self.adjacent = []
        self.tags = dict()

    def __repr__(self):
        return '(' + str(self.latitude) + ', ' + str(self.longitude) + '), ' + str(len(self.adjacent)) \
               + " adjacent nodes"

    def add_tag(self, key, value):
        self.tags[key] = value

    def add_adjacent(self, node, distance):
        self.adjacent.append((node, distance))
