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


# solver
def astar_solver_all(table_begin, table_end, width, s_kind):
    i_begin = 0
    i_end = 0
    children_beg = table_begin.all_positions
    children_end = table_end.all_positions
    start_time = datetime.datetime.now()
    print "**********"
    # deque = rij
    openset_begin = deque()
    closedset_begin = []
    current_begin = Node(table_begin.vehicles)
    openset_begin.append(current_begin)
    closedset_begin.append(table_retriever(width, current_begin.value))

    openset_end = deque()
    closedset_end = []
    current_end = Node(table_end.vehicles)
    openset_end.append(current_end)
    closedset_end.append(table_retriever(width, current_end.value))

    # main solver loop
    while len(openset_begin) > 0 and len(openset_end) > 0:
        # heuristieken gefilterd op keuze
        if s_kind == "block" or "taxi":
            current_begin = min(openset_begin, key=lambda o: o.score)
        if s_kind == "free" or "children":
            current_begin = max(openset_begin, key=lambda o: o.score)
        x_begin = deque()
        x_begin.append(table_retriever(width, current_begin.value))
        openset_begin.remove(current_begin)
        if x_begin not in closedset_begin:
            closedset_begin.append(x_begin)
        table_begin.vehicles = current_begin.value
        children = table_begin.move_vehicle()

        for child in children:
            y = table_retriever(width, child)
            if y in closedset_begin:
                continue
            node_begin = Node(child)
            if s_kind == "block":
                node_begin.score = find_blocking_cars(node_begin.value, width)
            if s_kind == "free":
                node_begin.score = find_free_path(node_begin.value, width)
            if s_kind == "taxi":
                node_begin.score = taxi_priority(node_begin.value, width)
            if s_kind == "children":
                node_begin.score = children_score(node_begin.value, width, children_beg)
            node_begin.parent = current_begin
            openset_begin.appendleft(node_begin)
            closedset_begin.append(y)
            i_begin =+ 1
            # De archive mag niet leeg zijn omdat ze anders overheen komen
            if len(closedset_begin) > 2:
                if y in closedset_end:
                    data_size = i_begin + i_end
                    game_win(start_time, current_begin, current_end, width, data_size)

        if s_kind == "block" or "taxi":
            current_end = min(openset_end, key=lambda o: o.score)
        if s_kind == "free" or "children":
            current_end = max(openset_end, key=lambda o: o.score)
        x_end = deque()
        x_end.append(table_retriever(width, current_end.value))
        openset_end.remove(current_end)
        if x_end not in closedset_end:
            closedset_end.append(x_end)
        table_end.vehicles = current_end.value
        children = table_end.move_vehicle()

        for child in children:
            y = table_retriever(width, child)
            if y in closedset_end:
                continue
            node_end = Node(child)
            if s_kind == "block":
                node_end.score = find_blocking_cars(node_end.value, width)
            if s_kind == "free":
                node_end.score = find_free_path(node_end.value, width)
            if s_kind == "taxi":
                node_end.score = taxi_priority(node_end.value, width)
            if s_kind == "children":
                node_end.score = children_score(node_end.value, width, children_end)
            node_end.parent = current_end
            openset_end.appendleft(node_end)
            closedset_end.append(y)
            i_end += 1
            # De archive mag niet leeg zijn omdat ze anders overheen komen
            if len(closedset_end) > 2:
                if y in closedset_begin:
                    data_size = i_begin + i_end
                    game_win(start_time, current_begin, current_end, width, data_size)