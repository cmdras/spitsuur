# coding=utf-8
import copy
from vehicle import vehicle

beginArchive = "@@"
endArchive = "!!"
count = 0

# hasher, nog niet geïmplementeerd maar misschien bruikbaar
def hasher(table):
    hashed = 0
    for i in table:
        for j in i:
            if j != ' ':
                hashed += 1
            hashed *= 10
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


# game_win checkt table op win conditie
def game_win_table_begin(archiveBegin):
    global beginArchive
    beginArchive = archiveBegin
    print beginArchive
    if game_win_total(beginArchive, endArchive):
        print "BEGIN: You win"
        return True
    else:
        return False


# game_win checkt table op win conditie
def game_win_table_end(archiveEnd):
    global endArchive
    endArchive = archiveEnd
    #print endArchive
    if game_win_total(beginArchive, endArchive):
        print "END: You win"
        return True
    else:
        return False


def game_win_total(beginArchive, endArchive):
    global count
    count += 1
    if count > 2:
        #print count
        for b in beginArchive:
            if b in endArchive:
                print "((((((", b, "=", endArchive, "))))))"
                print endArchive
                #if b == e:
                return True
    return False


# counter op levels of 'lagen' bij te houden
def myfuncBegin():
    myfuncBegin.counter += 1
    print "NodeBEGIN: ", myfuncBegin.counter

def myfuncEnd():
    myfuncEnd.counter += 1
    print "NodeEND: ", myfuncEnd.counter

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
            vehicle.age = 'o'
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
            for i in range(7 - x.length):
                positions.append(vehicle(x.id, i, x.col_v, x.orientation, x.board_size, x.age))
        elif x.orientation == "hor":
            for i in range(7 - x.length):
                positions.append(vehicle(x.id, x.row_v, i, x.orientation, x.board_size, x.age))
        vehicle_dict[x.id] = positions
    return vehicle_dict