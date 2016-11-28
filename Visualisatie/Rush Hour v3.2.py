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
            return self.items.pop()

    def flatten(self):
        self.items = list(itertools.chain.from_iterable(self.items))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class Board(Tkinter.Frame):
    def __init__(self, width, board_level):
        self.width = width
        self.height = width
        board_level = "vehicles/" + board_level + ".txt"
        self.vehicles = start_vehicles(board_level, width)

    # bouwt de table om te checken welke vehicles gemoved kunnen worden
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

    # Check welke vehicles gemoved kunnen worden en 'returned' een x aantal generators voor nieuwe tables
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

# breadth first solver
def solver(table):
    # preliminaries
    myfunc.counter = 0
    temp1 = []
    list_inter = []
    queue = Queue()
    archive = Queue()
    queue.insert(table.vehicles)
    archive.insert(queue.pop())
    children = table.move_vehicle()
    for i in children:
        queue.insert(i)
    # start main functie
    while True:
        # voor ieder item in queue check welke vehicles gemoved kunnen worden
        for i in queue.items:
            table.vehicles = i
            temp1.append(table.move_vehicle())
            # als i niet in archive zit wordt het in de archive geinsert (GEEN IDEE OF DIT DAADWERKELIJKE WERKT, MOET GECHECKED WORDEN)
            if i != archive.items:
                archive.insert(i)
        # bepaal lengte van queue voor later
        length = len(queue.items)
        print "Archive: ", len(archive.items)
        # main generator loop
        for j in temp1:
            for inter in j:
                # append iedere array met vehicles die uit de generator komt
                list_inter.append(inter)
                # check of array vehicles al in queue of archive zit (zelfde verhaal als hierboven, geen idee of dit ook daadwerkelijk werkt)
                # doe age_compare, zelfde vehicles met zelfde age, dan kan de laatste item in de queue verwijderd worden en de nieuwe worden aangesloten
                # dit werkt blijkbaar ook nog niet. Immers is de laatste item in de queue niet perse de 'vader' van inter
                if inter != queue.items and inter != archive.items:
                    if age_compare(inter, queue.items[-1]):
                        del queue.items[-1]
                    queue.insert(inter)
        # pop de queue'laag' (het zit al in de archive)
        for i in range(length):
            queue.pop()
        print "Queue: ", len(queue.items)
        myfunc()

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
    for j in list2:
        if j.age == 'n':
            b = j.id
    return a == b

# game_win checkt table op winconditie
def game_win(table):
    if table[2][5] == "T":
        return True
    else:
        return False

# start_vehicles is de start positie
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

# counter op levels of 'lagen' bij te houden
def myfunc():
    myfunc.counter += 1
    print "Level: ", myfunc.counter


start_rushhour()
