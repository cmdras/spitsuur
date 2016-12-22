# coding=utf-8
import copy
from vehicle import vehicle
import time
import datetime
import sys

# game_win checkt table op winconditie
def game_win(vehicle_array, width):
    for vehicle in vehicle_array:
        if vehicle.id == "T" and vehicle.col_v == width - 2:
            return True
    return False


# counter op levels of 'lagen' bij te houden
def myfunc():
    myfunc.counter += 1
    print "Level: ", myfunc.counter


# verwijdert oude auto van lijst en zet nieuwe auto erin
def add_new_car(vehicles, old_car, new_car):
    children = copy.copy(vehicles)
    children.remove(old_car)
    children.append(new_car)
    return children

# returnt een spelbord in de vorm van een matrix
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

# returnt alle mogelike posities van elke ingeladen vehicle
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

# heuristiek voor alle vehicles voor de taxi
def find_blocking_cars(vehicle_array, width):
    blocking_cars = 0
    board = table_retriever(width, vehicle_array)
    for i in range(width):
        for j in range(width):
            if board[i][j] == 'T':
                taxi_row = i
                taxi_col = j
                break
    for i in range((width - taxi_col - 2), width):
            if board[taxi_row][i] != ' ':
                blocking_cars += 1
    return blocking_cars

# heuristiek voor het zoeken van 1 a 2 vrije spaces voor de taxi
def find_free_path(vehicle_array, width):
    free_paths = 0
    board = table_retriever(width, vehicle_array)
    for i in range(width):
        for j in range(width):
            try:
                if board[i][j] == 'T' and board[i][j+2] == ' ':
                    free_paths += 1
                    try:
                        if board[i][j+3] == ' ':
                            free_paths += 1
                    except IndexError:
                        break
            except IndexError:
                free_paths += 1
                break
    return free_paths

# heuristiek voor het zoeken van 1 vrije space voor taxi
def taxi_priority(vehicle_array, width):

    blocking_score = find_free_path(vehicle_array, width)
    board = table_retriever(width, vehicle_array)
    for i in range(width):
        for j in range(width):
            if board[i][j] == 'T':
                taxi_row = i
                taxi_col = j
    if (taxi_col+2) < width and (taxi_col-1) >= 0:
        if (board[taxi_row][taxi_col + 2] != ' '):
            heuristic = -1
            return heuristic
    return blocking_score


# functie voor het vinden van het winnende pad, gegeven een node met het winpositie
def node_traversal(node):
    nodes = []
    while node.parent != None:
        nodes.append(node)
        node = node.parent
    return nodes

# returned alle mogelijke children van een bepaalde bordconfiguratie
def move_vehicle(vehicles, width, all_positions):
        table_queue = table_retriever(width, vehicles)
        for car in vehicles:
            if car.orientation == 'hor':
                if car.col_v - 1 >= 0 and table_queue[car.row_v][car.col_v - 1] == ' ':
                    for new_car in all_positions[car.id]:
                        if car.col_v - 1 == new_car.col_v:
                            children = add_new_car(vehicles, car, new_car)
                            yield children

                if car.col_v + car.length <= 5 and table_queue[car.row_v][car.col_v + car.length] == ' ':
                    for new_car in all_positions[car.id]:
                        if car.col_v + 1 == new_car.col_v:
                            children = add_new_car(vehicles, car, new_car)
                            yield children

            if car.orientation == 'ver':
                if car.row_v - 1 >= 0 and table_queue[car.row_v - 1][car.col_v] == ' ':
                    for new_car in all_positions[car.id]:
                        if car.row_v - 1 == new_car.row_v:
                            children = add_new_car(vehicles, car, new_car)
                            yield children

                if car.row_v + car.length <= 5 and table_queue[car.row_v + car.length][car.col_v] == ' ':
                    for new_car in all_positions[car.id]:
                        if car.row_v + 1 == new_car.row_v:
                            children = add_new_car(vehicles, car, new_car)
                            yield children

# heuristiek voor het aantal kinderen dat een bordconfiguratie kan maken
def children_score(vehicle_array, width, all_positions):
    children = move_vehicle(vehicle_array, width, all_positions)
    return sum(1 for x in children)
