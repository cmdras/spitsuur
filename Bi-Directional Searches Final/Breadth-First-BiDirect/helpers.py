# coding=utf-8
import copy
from vehicle import vehicle
import time
import datetime
import sys



# verwijdert oude auto van lijst en zet nieuwe auto erin
def add_new_car(vehicles, old_car, new_car):
    children = copy.copy(vehicles)
    children.remove(old_car)
    children.append(new_car)
    return children


# plaatst de vehicles op het bord
def table_retriever(width, vehicles):
        table = [[' ' for i in xrange(width)] for i in xrange(width)]
        for vehicle in vehicles:
            row_v, col_v = vehicle.row_v, vehicle.col_v
            if vehicle.orientation == 'hor':
                for i in range(vehicle.length):
                    table[row_v][col_v + i] = vehicle.id
            elif vehicle.orientation == 'ver':
                for i in range(vehicle.length):
                    table[row_v + i][col_v] = vehicle.id
        return table


# returnt alle mogelijke posities van elke ingeladen vehicle
# wordt gebruikt door move_vehicle()
def all_possible_vehicles(vehicles, width):
    vehicle_dict = {}
    for x in vehicles:
        positions = []
        if x.orientation == "ver":
            for i in range((width+1) - x.length):
                positions.append(vehicle(x.id, i, x.col_v, x.orientation, x.board_size))
        elif x.orientation == "hor":
            for i in range((width+1) - x.length):
                positions.append(vehicle(x.id, x.row_v, i, x.orientation, x.board_size))
        vehicle_dict[x.id] = positions
    return vehicle_dict


# haalt de stappen naar de oplossing terug
def node_traversal(node):
    nodes = []
    while node.parent != None:
        nodes.append(node)
        node = node.parent
    return nodes


# zorgt voor de weergave van essentiele informatie bij de gevonden oplossing
def game_win(tijd, stappen_begin, stappen_end, wijd, data_size):
    print "You win!"
    end_time = datetime.datetime.now()
    elapsed = end_time - tijd
    print "Time elapsed: " + str(elapsed.seconds) + " seconds and " + str(elapsed.microseconds) + " microseconds."
    winning_moves_begin = node_traversal(stappen_begin)
    winning_moves_end = node_traversal(stappen_end)
    winning_moves = winning_moves_begin + winning_moves_end
    print "Breadth First -> Bidirectional Search"
    print "Data Size: %d" %(data_size)
    print "number of moves: " + str(len(winning_moves))
    sys.exit()