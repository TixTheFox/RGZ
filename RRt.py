from Tree import *
from numpy import arange
import random
from math import sqrt
from wx import Point
from config import *
from sys import maxsize

obstacles = []

def cross_product(vec1: Vertex, vec2: Vertex):
    return vec1.x * vec2.y - vec1.y * vec2.x

def dot_product(vec1: Vertex, vec2: Vertex):
    return vec1.x * vec2.x + vec1.y * vec2.y


def segments_intersection(seg1_begin, seg1_end, seg2_begin, seg2_end):
    """
    checks intersection of segments [seg1_begin, seg1_end] and [seg2_begin, seg2_end] in R^2
    :return: True if intersects, False otherwise
    """
    denom = cross_product(seg1_end - seg1_begin, seg2_end - seg2_begin)
    alpha = cross_product(seg2_begin - seg1_begin, seg1_end - seg1_begin)
    beta = cross_product(seg2_begin - seg1_begin, seg2_end - seg2_begin)

    if denom == 0:
        if alpha != 0:
            return False
        t0 = dot_product(seg2_begin - seg1_begin, seg1_end - seg1_begin)
        t0 /= dot_product(seg1_end - seg1_begin, seg1_end - seg1_begin)

        t1 = t0 + dot_product(seg2_end - seg2_begin, seg1_end - seg1_begin)
        t1 /= dot_product(seg1_end - seg1_begin, seg1_end - seg1_begin)
        t0, t1 = min(t0, t1), max(t0, t1)
        if t1 < 0 or t0 > 1:
            return False

        return True

    if 0 <= alpha/denom <= 1 and 0 <= beta/denom <= 1:
        return True
    return False


def dist(vert1: Vertex, vert2: Vertex):
    return sqrt((vert1.x - vert2.x) ** 2 + (vert1.y - vert2.y) ** 2)


def collision_free(dot1, dot2):
    """
    Checks if segment [dot1, dot2] intersects with any obstacle
    :return: True, if no collision, False otherwise
    """
    if not dot1 == dot2:
        for i in obstacles:
            if any([
                    segments_intersection(dot1, dot2, i[0], i[1]),
                    segments_intersection(dot1, dot2, i[2], i[1]),
                    segments_intersection(dot1, dot2, i[0], i[2])
                    ]):
                return False
    return True


def nearest(tree, vertex):
    change_flag = False
    graph_vertices = tree.get_vertices()
    min_vert = tree.get_vertices()[0]
    min_dist = dist(vertex, min_vert)
    min_seg_dist = 1000000000
    min_seg_dot = 0
    for i in range(1, len(graph_vertices)):
        seg_begin, seg_end = graph_vertices[graph_vertices[i].parent], graph_vertices[i]
        geom_arg1 = dot_product(seg_end - vertex, seg_end - seg_begin)
        geom_arg2 = dot_product(seg_begin - vertex, seg_begin - seg_end)

        if geom_arg1 * geom_arg2 > 0:
            segment_normal = Vertex(seg_begin.y - seg_end.y, seg_end.x - seg_begin.x)
            segment_normal /= dist(segment_normal, Vertex(0, 0))
            if dot_product(segment_normal, seg_end - vertex) < 0:
                segment_normal *= -1

            # sin of one of the sharp angles
            result = geom_arg2 / (dist(seg_begin, vertex) * dist(seg_begin, seg_end))
            if result > 1:
                continue
            result = sqrt(1 - result ** 2)
            result = vertex + segment_normal * (result * dist(vertex, seg_begin))
            result.set_parent(i)
            result.round()

            if dist(result, vertex) < min_seg_dist:
                min_seg_dot = result
                min_seg_dist = dist(result, vertex)

        else:
            begin_dist, end_dist = dist(seg_begin, vertex), dist(seg_end, vertex)
            if begin_dist > end_dist:
                if end_dist < min_dist:
                    min_dist = end_dist
                    min_vert = seg_end
            else:
                if begin_dist < min_dist:
                    min_dist = begin_dist
                    min_vert = seg_begin

    if min_dist > min_seg_dist:
        saved_parent = min_seg_dot.parent
        tree.add(min_seg_dot)
        graph_vertices[-1].set_parent(graph_vertices[saved_parent].parent)
        graph_vertices[saved_parent].set_parent(len(graph_vertices) - 1)
        return min_seg_dot
    return min_vert


def steer(graph_vert: Vertex, rand_vertex: Vertex):
    current_dot = 0
    for i in arange(0, 1, 0.01):
        current_dot = (graph_vert - rand_vertex) * i + rand_vertex
        current_dot.round()
        if collision_free(graph_vert, current_dot):
            return current_dot


def nearest_to_end(tree, end_vert):
    min_vert = tree.get_vertices()[0]
    min_vert.set_parent(-1)
    min_dist = dist(min_vert, end_vert)
    for i in tree.get_vertices():
        if dist(i, end_vert) < min_dist and collision_free(i, end_vert):
            min_vert = i
            min_dist = dist(i, end_vert)

    if min_vert.parent == -1:
        end_vert.set_parent(-1)
        return end_vert
    return min_vert


def build_path(tree: Tree):
    current_vert = tree.get_vertices()[-1]
    if current_vert.parent == -1:
        return 0
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


def RRT(N, Qinit: Vertex, Qexit: Vertex, obst: list):
    """
    RRT
    :param N: number of iterations of building tree algorithm
    :param Qinit: starting dot
    :param Qexit: exit dot
    :return: list; consequence of dots which leads from Qinit to Qexit
    """
    global obstacles
    obstacles = obst
    Qinit.set_parent(-1)
    tree = Tree()
    tree.add(Qinit)

    random.seed(2036653558153635619)
    for i in range(N):
        if i == 220:
            pass
        Qrand = Vertex(random.randint(0, WIDTH), random.randint(0, HEIGHT), 0)
        try:
            Qnearest = nearest(tree, Qrand)
        except:
            raise ValueError
        Qsteered = steer(Qnearest, Qrand)

        if Qsteered:
            Qsteered.set_parent(tree.get_vertices().index(Qnearest))
            tree.add(Qsteered)

    Qnearest = nearest_to_end(tree, Qexit)
    if Qnearest.parent != -1:
        Qexit.set_parent(tree.get_vertices().index(Qnearest))
        tree.add(Qexit)
        result = transform_to_graphics(build_path(tree))
    else:
        result = 0
    return result, tree

