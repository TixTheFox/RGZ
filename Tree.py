class Vertex:
    def __init__(self, x, y, parent=0):
        self.x = x
        self.y = y
        self.parent = parent

    def __sub__(self, other):
        return Vertex(self.x - other.x, self.y - other.y, self.parent)

    def __add__(self, other):
        return Vertex(self.x + other.x, self.y + other.y, self.parent)

    def __mul__(self, number):
        return Vertex(int(self.x * number), int(self.y * number), self.parent)

    def set_parent(self, new_parent):
        self.parent = new_parent


class Tree:
    def __init__(self):
        self._vertices = []

    def add(self, vert: Vertex):
        self._vertices.append(vert)

    def get_vertices(self):
        return self._vertices
