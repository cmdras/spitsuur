import Tkinter
import itertools
import copy
import sys
import time

from vehicle import vehicle
from collections import deque
from helpers import *
from solvers import *


# class Board als infrastructuur voor solvers
# direction zorgt voor het 2 keer inladen van een eind en begin bestand
class Board(object):
    def __init__(self, width, board_level, direction):
        self.width = width
        self.height = width
        if direction == 0:
            board_level = "vehicles_BF/" + board_level + ".txt"
            self.vehicles = start_vehicles(board_level, width)
            self.all_positions = {}
            self.x = ''
        if direction == 1:
            board_level = "vehicles_BF/" + board_level + "BF_End.txt"
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
                            children = add_new_car(self.vehicles, car, new_car)
                            yield children

                # rechts check
                if car.col_v + car.length <= (self.width-1) and table_queue[car.row_v][car.col_v + car.length] == ' ':
                    for new_car in self.all_positions[car.id]:
                        if car.col_v + 1 == new_car.col_v:
                            children = add_new_car(self.vehicles, car, new_car)
                            yield children

            if car.orientation == 'ver':
                # boven check
                if car.row_v - 1 >= 0 and table_queue[car.row_v - 1][car.col_v] == ' ':
                    for new_car in self.all_positions[car.id]:
                        if car.row_v - 1 == new_car.row_v:
                            children = add_new_car(self.vehicles, car, new_car)
                            yield children

                # onder check
                if car.row_v + car.length <= (self.width-1) and table_queue[car.row_v + car.length][car.col_v] == ' ':
                    for new_car in self.all_positions[car.id]:
                        if car.row_v + 1 == new_car.row_v:
                            children = add_new_car(self.vehicles, car, new_car)
                            yield children


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


# start van het programma, neemt voorkeur mee bij oplossen
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

    board_begin = Board(board_size, game, 0)
    board_begin.all_positions = all_possible_vehicles(board_begin.vehicles, board_size)

    board_end = Board(board_size, game, 1)
    board_end.all_positions = all_possible_vehicles(board_end.vehicles, board_size)

    solverBF_BiDirect(board_begin, board_end, board_size)


start_rushhour()