import sys
import time
from vehicle import vehicle
from collections import deque
from helpers import *

# class om de parents en score bij te houden van een bordconfiguratie
class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.score = 0

# de A* solver
def astar_solver_all(table, width, s_kind):
    all_positions = table.all_positions
    visited = 0
    start_time = datetime.datetime.now()
    print "**********"
    openset = set()
    closedset = []

    current = Node(table.vehicles)
    openset.add(current)
    closedset.append(table_retriever(width, current.value))
    while openset:
        if s_kind == "block" or s_kind == "taxi":
            current = min(openset, key=lambda o: o.score)
        if s_kind == "free" or s_kind == "children":
            current = max(openset, key=lambda o: o.score)

        current = min(openset, key=lambda o: o.score)
        x = deque()
        x.append(table_retriever(width, current.value))     

        if game_win(current.value, width):
            print "You win!"
            end_time = datetime.datetime.now()
            elapsed = end_time - start_time
            print "Time elapsed: " + str(elapsed.seconds) + " seconds and " + str(elapsed.microseconds) + " microseconds."
            winning_moves = node_traversal(current)
            filename = s_kind + '_a1.txt'
            f = open(filename, 'w')
            for node in reversed(winning_moves):
                j = table_retriever(width, node.value)
                for x in j:
                    f.write(repr(x))
                    f.write("\n")
                f.write("--------------------\n")
            f.write(str(visited))
            f.write("\n")
            f.write("Time elapsed: " + str(elapsed.seconds) + " seconds and " + str(elapsed.microseconds) + " microseconds.")
            f.write("\n")
            f.write("number of moves: " + str(len(winning_moves)))


            f.close()
            print ">>> A Star"
            print "Data Size: %d" % (visited)
            print "number of moves: " + str(len(winning_moves))
            break
        
        openset.remove(current)
        if x not in closedset:
            closedset.append(x)
        table.vehicles = current.value
        children = table.move_vehicle()

        for child in children:
            y = table_retriever(width, child)
            if y in closedset:
                continue
            node = Node(child)
            if s_kind == "block":
                node.score = find_blocking_cars(node.value, width)
            if s_kind == "free":
                node.score = find_free_path(node.value, width)
            if s_kind == "taxi":
                node.score = taxi_priority(node.value, width)
            if s_kind == "children":
                node.score = children_score(child, width, all_positions)
            node.parent = current
            openset.add(node)
            closedset.append(y)
            visited += 1
            print visited