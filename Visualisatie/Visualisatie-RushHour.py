import Tkinter
from vehicle import vehicle

CAR_ID = {'A': 'cyan2', 'B': 'CadetBlue', 'C': 'RoyalBlue1',
          'D': 'dark orange', 'T': 'red2', ' ': 'grey'}

TRUCKS_ID = {'E': 'MediumPurple1', 'F': 'yellow2', 'Fa': 'yellow2',
             'G': 'gold', 'H': 'orange', 'I': 'gray64'}


class Board(Tkinter.Frame):
    def __init__(self, width, board_level):
        self.width = width
        self.height = width
        self.board_level = "vehicles/"+ board_level + ".txt"
        vehicles = []
        text_file = open(self.board_level, "r")
        lines = text_file.read().split('\n')
        for i in lines:
            j = i.split(',')
            vehicle_id = j[0]
            vehicle_row_v = j[1]
            vehicle_col_v = j[2]
            vehicle_or = j[3]
            vehicles.append(vehicle(vehicle_id, int(vehicle_row_v), int(vehicle_col_v), vehicle_or, self.width))
        table = table_retriever(vehicles, self.width)
        # format of informationboard
        # move_vehicles(table, vehicles)
        visualize(table, self.width, self.height)
        # prints the informationboard


def table_retriever(vehicles, size):
    
    
    table = [[' ' for i in xrange(size)] for i in xrange(size)]

    for vehicle in vehicles:
        row_v, col_v = vehicle.row_v, vehicle.col_v
        if vehicle.orientation == 'hor':
            for i in range(vehicle.length):
                table[row_v][col_v+i] = vehicle.id
        else:
            for i in range(vehicle.length):
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

# TODO
"""
def move_vehicles(table, vehicles):
    move_vehicle = []

    for vehicle in vehicles:
        if vehicle.orientation == 'hor' and vehicle.length < 3:
            if (table[vehicle.row_v][vehicle.col_v - 1]  == ' ' && vehicle.row_v > 0 && vehicle_row_v <= 5) or (table[vehicle.row_v][vehicle.col_v + 2] == ' ' && vehicle.row_v > 0 && vehicle_row_v <= 5):
                print '1'
                move_vehicle.append(vehicle)
        elif vehicle.orientation == 'hor':
            if (table[vehicle.row_v][vehicle.col_v -1] == ' ' && vehicle.row_v > 0 && vehicle_row_v <= 5) or (table[vehicle.row_v][vehicle.col_v + 3] == ' ' && vehicle.row_v > 0 && vehicle_row_v <= 5):
                print '2'
                move_vehicle.append(vehicle)
        elif vehicle.orientation == 'ver' and vehicle.length < 3:
            if (table[vehicle.row_v][vehicle.col_v - 1] == ' ' or table[vehicle.row_v + 2][vehicle.col_v] == ' ':
                print '3'
                move_vehicle.append(vehicle)
        elif vehicle.orientation == 'ver':
            if table[vehicle.row_v][vehicle.col_v - 1] == ' ' or table[vehicle.row_v][vehicle.col_v + 3] == ' ':
                print '4'
                move_vehicle.append(vehicle)

    print(move_vehicle)

"""

start_rushhour()
