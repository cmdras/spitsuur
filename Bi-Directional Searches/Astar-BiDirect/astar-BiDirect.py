import Tkinter
import itertools
import copy
import sys
import time

from vehicle import vehicle
from collections import deque
from helpers import *

CAR_ID = {'A': 'cyan2', 'B': 'CadetBlue', 'C': 'RoyalBlue1',
          'D': 'dark orange', 'T': 'red2', ' ': 'grey'}

TRUCKS_ID = {'E': 'MediumPurple1', 'F': 'yellow2', 'Fa': 'yellow2',
             'G': 'gold', 'H': 'orange', 'I': 'gray64'}

pick = ""

class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.score = 0


class Board(object):
    def __init__(self, width, board_level, direction, solver):
        self.width = width
        self.height = width
        first = solver.upper()
        first_letter_ext = first[:1]
        extension = "AS_%s_End.txt" % (first_letter_ext)
        if direction == 0:
            board_level = "vehicles_AS/" + board_level + ".txt"
            self.vehicles = start_vehicles(board_level, width)
            self.all_positions = {}
            self.x = ''
        if direction == 1:
            board_level = "vehicles_AS/" + board_level + extension
            self.vehicles = start_vehicles(board_level, width)
            self.all_positions = {}
            self.x = ''

    def table_retriever(self):
        table = [[' ' for i in xrange(self.width)] for i in xrange(self.width)]
        for vehicle in self.vehicles:
            row_v, col_v = vehicle.row_v, vehicle.col_v
            if vehicle.orientation == 'hor':
                for i in range(vehicle.length):
                    table[row_v][col_v + i] = vehicle.id
            elif vehicle.orientation == 'ver':
                for i in range(vehicle.length):
                    table[row_v + i][col_v] = vehicle.id
        if game_win(table):
            print "You Win!"
            sys.exit()
        return table

    def move_vehicle(self):
        self.x = table_retriever(self.width, self.vehicles)
        table_queue = self.x
        for car in self.vehicles:
            if car.orientation == 'hor':
                if car.col_v - 1 >= 0 and table_queue[car.row_v][car.col_v - 1] == ' ':
                    for new_car in self.all_positions[car.id]:
                        if car.col_v - 1 == new_car.col_v:
                            # vanaf hieronder kan in eigen functie
                            children = copy.deepcopy(self.vehicles)
                            children.remove(car)
                            children.append(new_car)
                            yield children

                if car.col_v + car.length <= self.width - 1 and table_queue[car.row_v][car.col_v + car.length] == ' ':
                    for new_car in self.all_positions[car.id]:
                        if car.col_v + 1 == new_car.col_v:
                            # vanaf hieronder kan in eigen functie
                            children = copy.copy(self.vehicles)
                            children.remove(car)
                            children.append(new_car)
                            yield children

            if car.orientation == 'ver':
                if car.row_v - 1 >= 0 and table_queue[car.row_v - 1][car.col_v] == ' ':
                    for new_car in self.all_positions[car.id]:
                        if car.row_v - 1 == new_car.row_v:
                            # vanaf hieronder kan in eigen functie
                            children = copy.copy(self.vehicles)
                            children.remove(car)
                            children.append(new_car)
                            yield children

                if car.row_v + car.length <= self.width - 1 and table_queue[car.row_v + car.length][car.col_v] == ' ':
                    for new_car in self.all_positions[car.id]:
                        if car.row_v + 1 == new_car.row_v:
                            # vanaf hieronder kan in eigen functie
                            children = copy.copy(self.vehicles)
                            children.remove(car)
                            children.append(new_car)
                            yield children


def astar_solver_all(table_begin, table_end, width, s_kind):
    i_begin = 0
    i_end = 0
    children_beg = table_begin.all_positions
    children_end = table_end.all_positions
    start_time = datetime.datetime.now()
    print "**********"
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

    while len(openset_begin) > 0 and len(openset_end) > 0:
        current_begin = min(openset_begin, key=lambda o: o.score)
        x_begin = deque()
        x_begin.append(table_retriever(width, current_begin.value))
        openset_begin.remove(current_begin)
        if x_begin not in closedset_begin:
            closedset_begin.append(x_begin)
        table_begin.vehicles = current_begin.value
        children = table_begin.move_vehicle()

        for child in children:
            y = table_retriever(width, child)
            if len(closedset_begin) > 2:
                if y in closedset_end:
                    data_size = i_begin + i_end
                    game_win(start_time, current_begin, current_end, width, data_size)
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

        current_end = min(openset_end, key=lambda o: o.score)
        x_end = deque()
        x_end.append(table_retriever(width, current_end.value))
        openset_end.remove(current_end)
        if x_end not in closedset_end:
            closedset_end.append(x_end)
        table_end.vehicles = current_end.value
        children = table_end.move_vehicle()

        for child in children:
            y = table_retriever(width, child)
            if len(closedset_end) > 2:
                if y in closedset_begin:
                    data_size = i_begin + i_end
                    game_win(start_time, current_begin, current_end, width, data_size)
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


def start_vehicles(board_level, width):
    vehicles = []
    text_file = open(board_level, "r")
    lines = text_file.read().split('\n')
    for i in lines:
        j = i.split(',')
        vehicle_id = j[0]
        vehicle_row_v = j[1]
        vehicle_col_v = j[2]
        vehicle_or = j[3]
        vehicles.append(vehicle(vehicle_id, int(vehicle_row_v), int(vehicle_col_v), vehicle_or, width))
    return vehicles


def start_rushhour():
    # type: () -> object
    a = 6
    b = 9
    c = 12
    print "Difficulty  1 = easy, 2 = normal, 3 = hard"
    print "A is 6*6, B is 9*9, C is 12*12"
    print "Choice option example: option_a1"
    while True:
        game = str(raw_input("Which board do you want to play?: "))
        if game[0] == "a" or game[0] == "b" or game[0] == "c":
            if game == "a1" or game == "a2" or game == "a3":
                board_size = a
            if game == "b1" or game == "b2" or game == "b3":
                board_size = b
            if game == "c":
                board_size = c
            break
    print "You can pick solver: block, free, taxi or children"
    solver = str(raw_input("which solver?: "))
    set_solver(solver)

    board_begin = Board(board_size, game, 0, solver)
    board_begin.all_positions = all_possible_vehicles(board_begin.vehicles, board_size)

    board_end = Board(board_size, game, 1, solver)
    board_end.all_positions = all_possible_vehicles(board_end.vehicles, board_size)

    astar_solver_all(board_begin, board_end, board_size, solver)

start_rushhour()
print "Exited"