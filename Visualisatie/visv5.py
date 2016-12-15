import Tkinter
import itertools
import copy
import sys
import threading
import parallelpy
from collections import deque

from multiprocessing import Process
from vehicle import vehicle
from helpers import *
from visv5End import *
from threading import Thread

CAR_ID = {'A': 'cyan2', 'B': 'CadetBlue', 'C': 'RoyalBlue1',
          'D': 'dark orange', 'T': 'red2', ' ': 'grey'}

TRUCKS_ID = {'E': 'MediumPurple1', 'F': 'yellow2', 'Fa': 'yellow2',
             'G': 'gold', 'H': 'orange', 'I': 'gray64'}


class BoardBegin(object):
    def __init__(self, width, board_level):
        self.width = width
        self.height = width
        board_level = "vehicles/" + board_level + ".txt"
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


def solverBegin(table, all_positions):
    myfuncBegin.counter = 0
    goal = 0
    table.all_positions = all_positions
    queueBegin = deque()
    archiveBegin = deque()
    pre = table.move_vehicle()
    archiveBegin.append(table.x)
    for i in pre:
        queueBegin.append(i)
    while True:
        table.vehicles = queueBegin .pop()
        if game_win_table_begin(archiveBegin) == True:
            print "You Win!"
            sys.exit()
        archiveBegin.append(table.x)
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
            if k not in queueBegin  and k not in archiveBegin:
                queueBegin.appendleft(k)
        myfuncBegin()


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

    def func1():
        boardBegin = BoardBegin(board_size, game)
        all_positionsBegin = all_possible_vehicles(boardBegin.vehicles, board_size)
        print "STARTED RUNNING SOLVERBEGIN"
        solverBegin(boardBegin, all_positionsBegin)

    def func2():
        boardEnd = BoardEnd(board_size, game)
        all_positionsEnd = all_possible_vehicles(boardEnd.vehicles, board_size)
        print "STARTED RUNNING SOLVEREND"
        solverEnd(boardEnd, all_positionsEnd)

    p = Process(target=func1)
    p.start()
    p2 = Process(target=func2)
    p2.start()
    # and so on
    p.join()
    p2.join()
    # the join means wait untill it finished



    #if __name__ == '__main__':
     #   Thread(target=func1).start()
      #  Thread(target=func2).start()

start_rushhour()