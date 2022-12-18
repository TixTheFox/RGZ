from Tree import *
from math import sqrt
from numpy import arange
import random
from wx import Point
from config import *


def cross_product(vec1: Vertex, vec2: Vertex):
    return vec1.x * vec2.y - vec1.y * vec2.x


def segments_intersection(seg1_begin, seg1_end, seg2_begin, seg2_end):
    """
    checks intersection of segments [seg1_begin, seg1_end] and [seg2_begin, seg2_end] in R^2
    :return: True if intersects, False otherwise
    """
    prod1 = cross_product(seg1_end - seg1_begin, seg2_end - seg1_begin)
    prod2 = cross_product(seg1_end - seg1_begin, seg2_begin - seg1_begin)

    if prod1 * prod2 <= 0:
        return True

    prod1 = cross_product(seg2_end - seg2_begin, seg1_end - seg2_begin)
    prod2 = cross_product(seg2_end - seg2_begin, seg1_begin - seg2_begin)

    if prod1 * prod2 <= 0:
        return True


    return False


def dist(vert1: Vertex, vert2: Vertex):
    return sqrt((vert1.x - vert2.x) ** 2 + (vert1.y - vert2.y) ** 2)


def collision_free(dot1, dot2):
    """
    Checks if segment [dot1, dot2] intersects with any obstacle
    :return: True, if no collision, False otherwise
    """
    for i in obstacles:
        if any([
                segments_intersection(dot1, dot2, i[0], i[1]),
                segments_intersection(dot1, dot2, i[2], i[1]),
                segments_intersection(dot1, dot2, i[0], i[2])
                ]):
            return False
    return True


def nearest(tree, vertex):
    min_vert = tree.get_vertices()[0]
    min_dist = dist(min_vert, vertex)
    for i in tree.get_vertices():
        current_dist = dist(i, vertex)
        if current_dist < min_dist:
            min_dist = current_dist
            min_vert = i

    return min_vert


def steer(graph_vert: Vertex, rand_vertex: Vertex):
    current_dot = 0
    for i in arange(0, 1, 0.01):
        current_dot = rand_vertex + (graph_vert - rand_vertex) * i
        if collision_free(graph_vert, current_dot):
            return current_dot


def nearest_to_end(tree, end_vert):
    min_vert = tree.get_vertices()[0]
    min_dist = dist(min_vert, end_vert)
    for i in tree.get_vertices():
        if dist(i, end_vert) < min_dist and collision_free(i, end_vert):
            min_vert = i
            min_dist = dist(i, end_vert)

    return min_vert


def build_path(tree: Tree):
    current_vert = tree.get_vertices()[-1]
    j = current_vert.parent
    path = [current_vert]
    while j != -1:
        path.append(tree.get_vertices()[j])
        j = path[-1].parent
    path.reverse()
    return path


def transform_to_graphics(obj):
    result = []

    for i in obj:
        result.append([Point(i.x, i.y), i.parent])

    return result


def RRT(N, Qinit: Vertex, Qexit: Vertex):
    """
    RRT
    :param N: number of iterations of building tree algorithm
    :param Qinit: starting dot
    :param Qexit: exit dot
    :return: list; consequence of dots which leads from Qinit to Qexit
    """

    tree = Tree()
    tree.add(Qinit)
    for i in range(N):
        Qrand = Vertex(random.randint(0, WIDTH), random.randint(0, HEIGHT), 0)
        Qnearest = nearest(tree, Qrand)
        Qsteered = steer(Qnearest, Qrand)
        Qsteered.set_parent(tree.get_vertices().index(Qnearest))
        tree.add(Qsteered)
    Qnearest = nearest_to_end(tree, Qexit)
    Qexit.set_parent(tree.get_vertices().index(Qnearest))
    tree.add(Qexit)
    result = transform_to_graphics(build_path(tree))
    return result

