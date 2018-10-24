class Way:
    def __init__(self, idNum):
        self.name = None
        self.id = idNum
        self.nodes = []
        self.tags = dict()

    def set_name(self, name):
        self.name = name

    def add_tag(self, key, value):
        self.tags[key] = value

    def add_node(self, node):
        self.nodes.append(node)