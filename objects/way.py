class Way:
    def __init__(self, idNum):
        self.name = None
        self.id = idNum
        self.nodes = []
        self.tags = dict()
        self.is_one_way = False

    def __repr__(self):
        print_val = self.name
        if self.is_one_way:
            print_val += " (1W)"
        print_val += " - " + str(len(self.nodes)) + " nodes"
        return print_val

    def set_name(self, name):
        self.name = name

    def add_tag(self, key, value):
        self.tags[key] = value

    def add_node(self, node):
        self.nodes.append(node)