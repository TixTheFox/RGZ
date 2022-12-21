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
        return Vertex(round(self.x * number, 5), round(self.y * number, 5), self.parent)

    def __truediv__(self, number):
        return Vertex(round(self.x / number, 5), round(self.y / number, 5), self.parent)

    def __eq__(self, other):
        return all([
            self.x == other.x,
            self.y == other.y,
            self.parent == other.parent
        ])

    def set_parent(self, new_parent):
        self.parent = new_parent

    def round(self):
        self.x, self.y = round(self.x), round(self.y)

class Tree:
    def __init__(self):
        self._vertices = []

    def add(self, vert: Vertex):
        try:
            self._vertices.index(vert)
        except ValueError:
            self._vertices.append(vert)
    def get_vertices(self):
        return self._vertices
