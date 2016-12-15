import Tkinter
import itertools
import copy
import sys
from collections import deque

from vehicle import vehicle
from helpers import *

CAR_ID = {'A': 'cyan2', 'B': 'CadetBlue', 'C': 'RoyalBlue1',
          'D': 'dark orange', 'T': 'red2', ' ': 'grey'}

TRUCKS_ID = {'E': 'MediumPurple1', 'F': 'yellow2', 'Fa': 'yellow2',
             'G': 'gold', 'H': 'orange', 'I': 'gray64'}


class BoardEnd(object):
    def __init__(self, width, board_level):
        self.width = width
        self.height = width
        board_level = "vehicles/" + board_level + "End.txt"
        self.vehicles = start_vehicles(board_level, width)
        self.all_positions = []
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
        else:
            return table

    def move_vehicle(self):
        self.x = self.table_retriever()
        table_queue = self.x
        for car in self.vehicles:
            if car.orientation == 'hor':
                if car.col_v - 1 >= 0 and table_queue[car.row_v][car.col_v - 1] == ' ':
                    for new_car in self.all_positions[car.id]:
                        if car.col_v - 1 == new_car.col_v:
                        # vanaf hieronder kan in eigen functie
                            children = copy.copy(self.vehicles)
                            children.remove(car)
                            children.append(new_car)
                            yield children

                if car.col_v + car.length <= 5 and table_queue[car.row_v][car.col_v + car.length] == ' ':
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

                if car.row_v + car.length <= 5 and table_queue[car.row_v + car.length][car.col_v] == ' ':
                    for new_car in self.all_positions[car.id]:
                        if car.row_v + 1 == new_car.row_v:
                        # vanaf hieronder kan in eigen functie
                            children = copy.copy(self.vehicles)
                            children.remove(car)
                            children.append(new_car)
                            yield children


def solverEnd(table, all_positions):
    myfuncEnd.counter = 0
    goal = 0
    table.all_positions = all_positions
    queueEnd = deque()
    archiveEnd = deque()
    pre = table.move_vehicle()
    archiveEnd.append(table.x)
    for i in pre:
        queueEnd.append(i)
    while True:
        table.vehicles = queueEnd.pop()
        if game_win_table_end(archiveEnd):
            print "You Win!"
            sys.exit()
        archiveEnd.append(table.x)
#        if goal == 0 and table.x[2][2] == 'T':
#            queue.clear()
#            goal = 1
#            print "Queue DUMPED"
#        if goal == 1 and table.x[2][1] == 'T':
#            queue.clear()
#            goal = 2
#            print "Queue DUMPED"
#        if goal == 2 and table.x[2][0] == 'T':
#            queue.clear()
#            goal = 3
#            print "Queue DUMPED"
        pre = table.move_vehicle()
        for k in pre:
            if 'T25hor' in k:
                game_win()
            if k not in queueEnd and k not in archiveEnd:
                queueEnd.appendleft(k)
        myfuncEnd()


def game_win():
    print "You Win!"
    sys.exit()

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
        vehicles.append(vehicle(vehicle_id, int(vehicle_row_v), int(vehicle_col_v), vehicle_or, width, 'o'))
    return vehicles

