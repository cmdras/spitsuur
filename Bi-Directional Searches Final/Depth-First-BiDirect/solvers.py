import sys
import time
from vehicle import vehicle
from collections import deque
from helpers import *


# Class om de parents en de score bij te houden van een bordconfiguratie
class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.score = 0

# solver voor Bidirectional: Depth First > < Depth First
def solver_DepthDepth(table_begin, table_end, width):
    i_begin = 0
    i_end = 0
    start_time = datetime.datetime.now()
    print "**********"
    # deque = rij
    openset_begin = deque()
    # set = archive
    closedset_begin = set()
    current_begin = Node(table_begin.vehicles)
    openset_begin.append(current_begin)

    openset_end = deque()
    closedset_end = set()
    current_end = Node(table_end.vehicles)
    openset_end.append(current_end)

    # main solver loop
    while len(openset_begin) > 0 and len(openset_end) > 0:
        current_begin = openset_begin.pop()
        x_begin = (table_retriever(width, current_begin.value))
        closedset_begin.add(repr(x_begin))
        table_begin.vehicles = current_begin.value
        children = table_begin.move_vehicle()
        for child in children:
            y = table_retriever(width, child)
            y = repr(y)
            if y in closedset_begin:
                continue
            node_begin = Node(child)
            node_begin.parent = current_begin
            openset_begin.append(node_begin)
            closedset_begin.add(y)
            i_begin += 1
            # De archive mag niet leeg zijn omdat ze anders overheen komen
            if len(closedset_begin) > 2:
                if y in closedset_end:
                    data_size = i_begin + i_end
                    game_win(start_time, current_begin, current_end, width, data_size)

        current_end = openset_end.pop()
        x_end = (table_retriever(width, current_end.value))
        closedset_end.add(repr(x_end))
        table_end.vehicles = current_end.value
        children = table_end.move_vehicle()
        for child in children:
            y = table_retriever(width, child)
            y = repr(y)
            if y in closedset_end:
                continue
            node_end = Node(child)
            node_end.parent = current_begin
            openset_end.append(node_end)
            closedset_end.add(y)
            i_end += 1
            # De archive mag niet leeg zijn omdat ze anders overheen komen
            if len(closedset_end) > 2:
                if y in closedset_begin:
                    data_size = i_begin + i_end
                    game_win(start_time, current_begin, current_end, width, data_size)


# solver voor Bidirectional: Depth First > < Breadth First
def solver_DepthBreadth(table_begin, table_end, width):
    i_begin = 0
    i_end = 0
    start_time = datetime.datetime.now()
    print "**********"
    # deque = rij
    openset_begin = deque()
    # set = archive
    closedset_begin = set()
    current_begin = Node(table_begin.vehicles)
    openset_begin.append(current_begin)

    openset_end = deque()
    closedset_end = set()
    current_end = Node(table_end.vehicles)
    openset_end.append(current_end)

    # main solver loop
    while len(openset_begin) > 0 and len(openset_end) > 0:
        current_begin = openset_begin.pop()
        x_begin = (table_retriever(width, current_begin.value))
        closedset_begin.add(repr(x_begin))
        table_begin.vehicles = current_begin.value
        children = table_begin.move_vehicle()
        for child in children:
            y = table_retriever(width, child)
            y = repr(y)
            if y in closedset_begin:
                continue
            node_begin = Node(child)
            node_begin.parent = current_begin
            openset_begin.append(node_begin)
            closedset_begin.add(y)
            i_begin += 1
            # De archive mag niet leeg zijn omdat ze anders overheen komen
            if len(closedset_begin) > 2:
                if y in closedset_end:
                    data_size = i_begin + i_end
                    game_win(start_time, current_begin, current_end, width, data_size)

        current_end = openset_end.pop()
        table_end.vehicles = current_end.value
        children_end = table_end.move_vehicle()
        for child in children_end:
            y = table_retriever(width, child)
            y = repr(y)
            if y in closedset_end:
                continue
            node_end = Node(child)
            node_end.parent = current_end
            openset_end.appendleft(node_end)
            closedset_end.add(y)
            i_end += 1
            # De archive mag niet leeg zijn omdat ze anders overheen komen
            if len(closedset_end) > 2:
                if y in closedset_begin:
                    data_size = i_begin + i_end
                    game_win(start_time, current_begin, current_end, width, data_size)


# solver voor Bidirectional: Breadth First > < Depth First
def solver_BreadthDepth(table_begin, table_end, width):
    i_begin = 0
    i_end = 0
    start_time = datetime.datetime.now()
    print "**********"
    # deque = rij
    openset_begin = deque()
    # set = archive
    closedset_begin = set()
    current_begin = Node(table_begin.vehicles)
    openset_begin.append(current_begin)

    openset_end = deque()
    closedset_end = set()
    current_end = Node(table_end.vehicles)
    openset_end.append(current_end)

    # main solver loop
    while len(openset_begin) > 0 and len(openset_end) > 0:
        current_begin = openset_begin.pop()
        table_begin.vehicles = current_begin.value
        children_begin = table_begin.move_vehicle()
        for child in children_begin:
            y = table_retriever(width, child)
            y = repr(y)
            if y in closedset_begin:
                continue
            node_begin = Node(child)
            node_begin.parent = current_begin
            openset_begin.appendleft(node_begin)
            closedset_begin.add(y)
            i_begin += 1
            # De archive mag niet leeg zijn omdat ze anders overheen komen
            if len(closedset_begin) > 2:
                if y in closedset_end:
                    print "BREADTH WINT"
                    print i_begin
                    print i_end
                    data_size = i_begin + i_end
                    game_win(start_time, current_begin, current_end, width, data_size)

        current_end = openset_end.pop()
        table_end.vehicles = current_end.value
        children = table_end.move_vehicle()
        for child in children:
            y = table_retriever(width, child)
            y = repr(y)
            if y in closedset_end:
                continue
            node_end = Node(child)
            node_end.parent = current_begin
            openset_end.append(node_end)
            closedset_end.add(y)
            i_end += 1
            # De archive mag niet leeg zijn omdat ze anders overheen komen
            if len(closedset_end) > 2:
                if y in closedset_begin:
                    print "DEPTH WINT"
                    print i_begin
                    print i_end
                    data_size = i_begin + i_end
                    game_win(start_time, current_begin, current_end, width, data_size)
