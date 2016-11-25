import Tkinter
import itertools
import copy

from vehicle import vehicle

CAR_ID = {'A': 'cyan2', 'B': 'CadetBlue', 'C': 'RoyalBlue1',
          'D': 'dark orange', 'T': 'red2', ' ': 'grey'}

TRUCKS_ID = {'E': 'MediumPurple1', 'F': 'yellow2', 'Fa': 'yellow2',
             'G': 'gold', 'H': 'orange', 'I': 'gray64'}

# creeer een class genaamd Queue met de volgende methods:__init__, insert en remove(pop)
class Queue:
    """ Represents a queue. """
    def __init__(self):
        self.items = []

    def insert(self, other):
        self.items.append(other)

    def pop(self):
        if self.items is []:
            return 'The queue is empty'
        else:
            return self.items.pop(0)

    def flatten(self):
        self.items = list(itertools.chain.from_iterable(self.items))


class Board(Tkinter.Frame):
    def __init__(self, width, board_level):
        self.width = width
        self.height = width
        board_level = "vehicles/" + board_level + ".txt"
        self.vehicles = start_vehicles(board_level, width)

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
            vehicle.age = 'o'
        if game_win(table):
            print "You Win!"
        return table

    def move_vehicle(self):
        table_queue = self.table_retriever()
        for car in self.vehicles:
            if car.orientation == 'hor':
                if car.col_v - 1 >= 0 and table_queue[car.row_v][car.col_v - 1] == ' ':
                    new_car = vehicle(car.id, car.row_v, car.col_v - 1, car.orientation, 6, 'n')
                    # vanaf hieronder kan in eigen functie

                    children = copy.copy(self.vehicles)
                    children.remove(car)
                    children.append(new_car)
                    yield children

                if car.col_v + car.length <= 5 and table_queue[car.row_v][car.col_v + car.length] == ' ':
                    new_car = vehicle(car.id, car.row_v, car.col_v + 1, car.orientation, 6, 'n')
                    # vanaf hieronder kan in eigen functie

                    children = copy.copy(self.vehicles)
                    children.remove(car)
                    children.append(new_car)
                    yield children

            if car.orientation == 'ver':
                if car.row_v - 1 >= 0 and table_queue[car.row_v - 1][car.col_v] == ' ':
                    new_car = vehicle(car.id, car.row_v - 1, car.col_v, car.orientation, 6, 'n')
                    # vanaf hieronder kan in eigen functie

                    children = copy.copy(self.vehicles)
                    children.remove(car)
                    children.append(new_car)
                    yield children

                if car.row_v + car.length <= 5 and table_queue[car.row_v + car.length][car.col_v] == ' ':
                    new_car = vehicle(car.id, car.row_v + 1, car.col_v, car.orientation, 6, 'n')
                    # vanaf hieronder kan in eigen functie

                    children = copy.copy(self.vehicles)
                    children.remove(car)
                    children.append(new_car)
                    yield children

def solver(table):
    myfunc.counter = 0
    temp1 = []
    list_inter = []
    queue = Queue()
    archive = Queue()
    queue.insert(table.vehicles)
    archive.insert(table.vehicles)
    children = table.move_vehicle()
    for i in children:
        queue.insert(i)
    while True:
        for i in queue.items:
            table.vehicles = i
            temp1.append(table.move_vehicle())
            for j in archive.items:
                if j != table.vehicles:
                    archive.insert(queue.pop())
                    break
            else:
                queue.pop()
        print "Archive: ", len(archive.items)
        for j in temp1:
            for inter in j:
                list_inter.append(inter)
                if inter != queue.items:
                    if age_compare(inter, queue.items[-1]):
                        queue.pop()
                    queue.insert(inter)
        print "Queue: ", len(queue.items)
        myfunc()

def age_compare(list1, list2):
    for i in list1:
        if i.age == 'o':
            a = i.id
    for j in list2:
        if j.age == 'o':
            b = j.id
    return a != b


def game_win(table):
    if table[2][5] == "T":
        return True
    else:
        return False

def start_vehicles(board_level, width):
    vehicles = []
    text_file = open(board_level, "r")
    lines = text_file.read().split('\n')
    for i in lines:
        j = i.split(',')
        vehicle_id = j[0]
        vehicle_row_v = j[2]
        vehicle_col_v = j[1]
        vehicle_or = j[3]
        vehicles.append(vehicle(vehicle_id, int(vehicle_row_v), int(vehicle_col_v), vehicle_or, width, 'o'))
    return vehicles

def start_rushhour():
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
    solver(board)

def myfunc():
    myfunc.counter += 1
    print "Level: ", myfunc.counter


start_rushhour()