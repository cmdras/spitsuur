# coding=utf-8
import copy
from vehicle import vehicle
import time
import datetime
import sys


# hasher, nog niet geïmplementeerd maar misschien bruikbaar
def hasher(vehicles):
    hashed = ''
    for i in vehicles:
        a = str(i.id)
        b = str(i.row_v)
        c = str(i.col_v)
        d = str(i.length)
        e = str(i.orientation)
        hashed += a + b + c + d + e
    return hashed


# age_compare, check de eigenschappen van twee vehicles en de id, als match dan return true
def age_compare(list1, list2):
    for i in list1:
        if i.age == 'n':
            a = i.id
        else:
            return False
    for j in list2:
        if j.age == 'n':
            b = j.id
        else:
            return False
    return a == b


# game_win checkt table op winconditie
def game_win(table):
    if table[2][5] == "T":
        return True
    else:
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


def board_vehicles(vehicles):
    string = []
    for i in vehicles:
        string.append(i.id)

    return string


def vehicles_to_string(vehicles, board_vehicles):
    string = ""
    for i in range(len(board_vehicles)):
        for j in vehicles:
            if board_vehicles[i] == j.id:
                string += str(j.row_v)
                string += str(j.col_v)
    return string


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


def node_traversal(node):
    nodes = []
    while node.parent != None:
        nodes.append(node)
        node = node.parent
    return nodes

def move_vehicle(vehicles, width, all_positions):
        table_queue = table_retriever(width, vehicles)
        for car in vehicles:
            if car.orientation == 'hor':
                if car.col_v - 1 >= 0 and table_queue[car.row_v][car.col_v - 1] == ' ':
                    for new_car in all_positions[car.id]:
                        if car.col_v - 1 == new_car.col_v:
                            # vanaf hieronder kan in eigen functie
                            children = copy.deepcopy(vehicles)
                            children.remove(car)
                            children.append(new_car)
                            yield children

                if car.col_v + car.length <= 5 and table_queue[car.row_v][car.col_v + car.length] == ' ':
                    for new_car in all_positions[car.id]:
                        if car.col_v + 1 == new_car.col_v:
                            # vanaf hieronder kan in eigen functie
                            children = copy.copy(vehicles)
                            children.remove(car)
                            children.append(new_car)
                            yield children

            if car.orientation == 'ver':
                if car.row_v - 1 >= 0 and table_queue[car.row_v - 1][car.col_v] == ' ':
                    for new_car in all_positions[car.id]:
                        if car.row_v - 1 == new_car.row_v:
                            # vanaf hieronder kan in eigen functie
                            children = copy.copy(vehicles)
                            children.remove(car)
                            children.append(new_car)
                            yield children

                if car.row_v + car.length <= 5 and table_queue[car.row_v + car.length][car.col_v] == ' ':
                    for new_car in all_positions[car.id]:
                        if car.row_v + 1 == new_car.row_v:
                            # vanaf hieronder kan in eigen functie
                            children = copy.copy(vehicles)
                            children.remove(car)
                            children.append(new_car)
                            yield children

def children_score(vehicle_array, width, all_positions):
    children = move_vehicle(vehicle_array, width, all_positions)
    return sum(1 for x in children)
