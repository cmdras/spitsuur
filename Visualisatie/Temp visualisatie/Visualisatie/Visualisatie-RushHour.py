import Tkinter
import itertools
import copy
from vehicle import vehicle

CAR_ID = {'A': 'cyan2', 'B': 'CadetBlue', 'C': 'RoyalBlue1',
          'D': 'dark orange', 'T': 'red2', ' ': 'grey'}

TRUCKS_ID = {'E': 'MediumPurple1', 'F': 'yellow2', 'Fa': 'yellow2',
             'G': 'gold', 'H': 'orange', 'I': 'gray64'}

# creeer een class genaamd Queue met de volgende methods:__init__, insert en remove
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
        self.board_level = "vehicles/" + board_level + ".txt"
        vehicles = []
        text_file = open(self.board_level, "r")
        lines = text_file.read().split('\n')
        for i in lines:
            j = i.split(',')
            vehicle_id = j[0]
            vehicle_row_v = j[2]
            vehicle_col_v = j[1]
            vehicle_or = j[3]
            vehicles.append(vehicle(vehicle_id, int(vehicle_row_v), int(vehicle_col_v), vehicle_or, self.width))

        id_list = id_lister(vehicles)
        # move
        myfunc.counter = 0
        archive = Queue()
        queue = Queue()
        start_table = table_retriever(vehicles, self.width)
        queue.insert(start_table)
        children_level = move_vehicle(archive, queue, id_list)
        children_level_former(queue, children_level)
        archive.insert(queue.pop())
        while True:
            cool = len(children_level)
            children_level = move_vehicle(archive, queue, id_list)
            children_level_former(queue, children_level)
            for i in range(cool):
                archive.insert(queue.pop())
#            if child = win_pos
#                print "You have won!"
#                break
#            visualize(table, self.width, self.height)
        # prints the informationboard


def table_retriever(vehicles, size):
    table = [[' ' for i in xrange(size)] for i in xrange(size)]

    for vehicle in vehicles:
        row_v, col_v = vehicle.row_v, vehicle.col_v
        if vehicle.orientation == 'hor':
            for i in range(vehicle.length + 1):
                table[row_v][col_v+i] = vehicle.id
        elif vehicle.orientation == 'ver':
            for i in range(vehicle.length + 1):
                table[row_v+i][col_v] = vehicle.id
    return table


def visualize(table, width, height):
    canvas = Tkinter.Tk()
    for r in range(width):
        for c in range(height):
            if table[r][c][0] in CAR_ID:
                Tkinter.Label(canvas, text=(table[r][c]), borderwidth=20, background=CAR_ID[table[r][c][0]]).grid(row=r, column=c)
            else:
                Tkinter.Label(canvas, text=(table[r][c]), borderwidth=20, background=TRUCKS_ID[table[r][c][0]]).grid(row=r, column=c)
    canvas.mainloop()

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
    Board(board_size, game)

def move_vehicle(archive, queue, id_list):
    children = []
    table_list = copy.deepcopy(queue.items)
    for table_queue in table_list:
        checked = []
        for r in range(6):
            for c in range(6):
                new_table = copy.deepcopy(table_queue)
                if table_queue[r][c] is not ' ':
                    if table_queue[r][c] in id_list and table_queue[r][c] not in TRUCKS_ID:
                        id = str(table_queue[r][c])
                        length = 2
                    elif table_queue[r][c] in TRUCKS_ID:
                        id = str(table_queue[r][c])
                        length = 3
                    if id in checked:
                        continue
                    elif id not in checked:
                        checked.append(id)
                    try:
                        if table_queue[r][c+1] == table_queue[r][c]:
                            if c-1 >= 0 and table_queue[r][c-1] == ' ':
                                new_table[r][c + (length-1)] = ' '
                                for i in range(length):
                                    new_table[r][(c-1)+i] = id
                                if new_table not in queue.items and new_table not in children and new_table not in archive.items:
                                    children.append(new_table)

                            new_table = table_queue
                            if c+length <= 5 and table_queue[r][c+length] == ' ':
                                new_table[r][c] = ' '
                                for i in range(length):
                                    new_table[r][(c+1) + i] = table_queue[r][c]
                                if new_table not in queue.items and new_table not in children and new_table not in archive.items:
                                    children.append(new_table)

                        elif table_queue[r+1][c] == table_queue[r][c]:
                            if r-1 >= 0 and table_queue[r-1][c] == ' ':
                                new_table[r + (length-1)][c] = ' '
                                for i in range(length):
                                    new_table[(r-1)+i][c] = id
                                if new_table not in queue.items and new_table not in children and new_table not in archive.items:
                                    children.append(new_table)

                            new_table = table_queue
                            if table_queue[r+length][c] == ' ':
                                new_table[r][c] = ' '
                                for i in range(length):
                                    new_table[(r+1) + i][c] = id
                                if new_table not in queue.items and new_table not in children and new_table not in archive.items:
                                    children.append(new_table)
                    except IndexError:
                        checked.append(id)
                        continue
        myfunc()
    return children


def id_lister(vehicles):
    id_list = []
    for vehicle in vehicles:
        id_list.append(vehicle.id)
    return id_list

def game_win(table):
    if table[2][5] == "T":
        print 'WIN!'

def myfunc():
    myfunc.counter += 1
    print myfunc.counter


def bfs(archive, start):
    archive, queue = set(), [start]
    while queue:
        last_item_queue = queue.pop(0)
        if last_item_queue not in archive:
            archive.add(last_item_queue)
            queue.insert(new_gs)
    return visited

def children_level_former(queue, children_level):
    for i in children_level:
        game_win(i)
        queue.insert(i)



start_rushhour()
