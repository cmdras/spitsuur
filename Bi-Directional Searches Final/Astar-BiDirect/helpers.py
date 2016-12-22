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


# Heuristiek voor alle voor de taxi
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


# Heuristiek voor het zoeken van 1 a 2 vrije spaces voor de taxi
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


# heuristiek voor het zoeken van 1 vrije space voor de taxi
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


# returned alle mogelijke children speciaal voor de children heuristiek
def move_vehicle(vehicles, width, all_positions):
        table_queue = table_retriever(width, vehicles)
        for car in vehicles:
            if car.orientation == 'hor':
                if car.col_v - 1 >= 0 and table_queue[car.row_v][car.col_v - 1] == ' ':
                    for new_car in all_positions[car.id]:
                        if car.col_v - 1 == new_car.col_v:
                            children = copy.deepcopy(vehicles)
                            children.remove(car)
                            children.append(new_car)
                            yield children

                if car.col_v + car.length <= 5 and table_queue[car.row_v][car.col_v + car.length] == ' ':
                    for new_car in all_positions[car.id]:
                        if car.col_v + 1 == new_car.col_v:
                            children = copy.copy(vehicles)
                            children.remove(car)
                            children.append(new_car)
                            yield children

            if car.orientation == 'ver':
                if car.row_v - 1 >= 0 and table_queue[car.row_v - 1][car.col_v] == ' ':
                    for new_car in all_positions[car.id]:
                        if car.row_v - 1 == new_car.row_v:
                            children = copy.copy(vehicles)
                            children.remove(car)
                            children.append(new_car)
                            yield children

                if car.row_v + car.length <= 5 and table_queue[car.row_v + car.length][car.col_v] == ' ':
                    for new_car in all_positions[car.id]:
                        if car.row_v + 1 == new_car.row_v:
                            children = copy.copy(vehicles)
                            children.remove(car)
                            children.append(new_car)
                            yield children


# heuristiek voor het aantal kinderen dat een bord configiratie kan maken
def children_score(vehicle_array, width, all_positions):
    children = move_vehicle(vehicle_array, width, all_positions)
    return sum(1 for x in children)


# haalt de stappen naar de oplossing terug
def node_traversal(node):
    nodes = []
    while node.parent != None:
        nodes.append(node)
        node = node.parent
    return nodes


# zet de print statement voor de resultaten klaar
def set_solver(solver_pick):
    global pick
    if solver_pick == "block":
        pick = "A Star: Block -> Bidirectional Search"
    if solver_pick == "free":
        pick = "A Star: Free -> Bidirectional Search"
    if solver_pick == "taxi":
        pick = "A Star: Taxi -> Bidirectional Search"
    if solver_pick == "children":
        pick = "A Star: Children -> Bidirectional Search"


# zorgt voor de weergave van essentiele informatie bij de gevonden oplossing
def game_win(tijd, stappen_begin, stappen_end, wijd, data_size):
    print "You win!"
    end_time = datetime.datetime.now()
    elapsed = end_time - tijd
    print "Time elapsed: " + str(elapsed.seconds) + " seconds and " + str(elapsed.microseconds) + " microseconds."
    winning_moves_begin = node_traversal(stappen_begin)
    winning_moves_end = node_traversal(stappen_end)
    winning_moves = winning_moves_begin + winning_moves_end
    global pick
    print pick
    print "Data Size: %d" %(data_size)
    print "number of moves: " + str(len(winning_moves))
    sys.exit()