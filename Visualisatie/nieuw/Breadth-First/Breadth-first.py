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


# creeer een class genaamd node, met eigenschappen: value en parant
class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None


# class Board als infrastructuur voor solvers
class Board(object):
    def __init__(self, width, board_level):
        self.width = width
        self.height = width
        board_level = "vehicles/" + board_level + ".txt"
        self.vehicles = start_vehicles(board_level, width)
        self.all_positions = {}
        self.x = ''

    # functie om de 2d array te bouwen op basis van de vehicle array
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

    # functie om de children te yielden
    def move_vehicle(self):
        self.x = table_retriever(self.width, self.vehicles)
        table_queue = self.x
        for car in self.vehicles:
            if car.orientation == 'hor':
                # links check
                if car.col_v - 1 >= 0 and table_queue[car.row_v][car.col_v - 1] == ' ':
                    for new_car in self.all_positions[car.id]:
                        if car.col_v - 1 == new_car.col_v:
                            children = copy.deepcopy(self.vehicles)
                            children.remove(car)
                            children.append(new_car)
                            yield children
                # rechts check
                if car.col_v + car.length <= (self.width-1) and table_queue[car.row_v][car.col_v + car.length] == ' ':
                    for new_car in self.all_positions[car.id]:
                        if car.col_v + 1 == new_car.col_v:
                            children = copy.copy(self.vehicles)
                            children.remove(car)
                            children.append(new_car)
                            yield children

            if car.orientation == 'ver':
                # boven check
                if car.row_v - 1 >= 0 and table_queue[car.row_v - 1][car.col_v] == ' ':
                    for new_car in self.all_positions[car.id]:
                        if car.row_v - 1 == new_car.row_v:
                            children = copy.copy(self.vehicles)
                            children.remove(car)
                            children.append(new_car)
                            yield children

                # onder check
                if car.row_v + car.length <= (self.width-1) and table_queue[car.row_v + car.length][car.col_v] == ' ':
                    for new_car in self.all_positions[car.id]:
                        if car.row_v + 1 == new_car.row_v:
                            children = copy.copy(self.vehicles)
                            children.remove(car)
                            children.append(new_car)
                            yield children

# solver
def breadth_first_solver(table, width):
    i = 0
    start_time = datetime.datetime.now()
    print "**********"
    # deque = rij
    openset = deque()
    # set = archive
    closedset = set()
    current = Node(table.vehicles)
    openset.append(current)
    # main solver loop
    while openset:
        current = openset.pop()
        if game_win2(current.value):
            print "You win!"
            end_time = datetime.datetime.now()
            elapsed = end_time - start_time
            print "Time elapsed: " + str(elapsed.seconds) + " seconds and " + str(elapsed.microseconds) + " microseconds."
            winning_moves = node_traversal(current)
            f = open('A33bf.txt', 'w')
            # schrijf naar .txt voor archivering resultaten
            for node in reversed(winning_moves):
                j = table_retriever(width, node.value)
                for x in j:
                    f.write(repr(x))
                    f.write("\n")
                f.write("--------------------\n")
            f.write("Time elapsed: " + str(elapsed.seconds) + " seconds and " + str(elapsed.microseconds) + " microseconds.\n")
            f.write("number of moves: " + str(len(winning_moves)))
            f.close()
            print "number of moves: " + str(len(winning_moves))
            break

        table.vehicles = current.value
        children = table.move_vehicle()
        # Voor ieder kind in children check of ze in archive zitten en voeg evt. toe aan archive
        for child in children:
            y = table_retriever(width, child)
            y = repr(y)
            if y in closedset:
                continue
            node = Node(child)
            node.parent = current
            openset.appendleft(node)
            closedset.add(y)
            i += 1
            print i


# aanpassen voor a,b en c borden (a=4,b=7,c=10)
def game_win2(vehicle_array):
    for vehicle in vehicle_array:
        if vehicle.id == "T" and vehicle.col_v == 7:
            return True
    return False

# laden van het startpunt
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
    board = Board(board_size, game)
    board.all_positions = all_possible_vehicles(board.vehicles, board_size)
    breadth_first_solver(board, board_size)


start_rushhour()
