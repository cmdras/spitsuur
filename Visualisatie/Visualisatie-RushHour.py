import Tkinter
from vehicle import vehicle

CAR_ID = {'A': 'green', 'B': 'CadetBlue', 'C': 'RoyalBlue1',
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
            vehicle_x = j[1]
            vehicle_y = j[2]
            vehicle_or = j[3]
            #print vehicle_id
            vehicles.append(vehicle(vehicle_id, int(vehicle_x), int(vehicle_y), vehicle_or, self.width))
        #print vehicles
        table = table_retriever(vehicles, self.width)
        # format of informationboard
        visualize(table, self.width, self.height)
        # prints the informationboard


def table_retriever(vehicles, size):
    
    """
    table = [[' ' for i in xrange(size)] for i in xrange(size)]

    """
    table = [[' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ']]
    
    for vehicle in vehicles:
        x, y = vehicle.x, vehicle.y
        if vehicle.orientation == 'hor':
            for i in range(vehicle.length):
                table[x][y+i] = vehicle.id
        else:
            for i in range(vehicle.length):
                table[x+i][y] = vehicle.id
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
    a1 = 6
    a2 = 6
    a3 = 6
    b1 = 9
    b2 = 9
    b3 = 9
    c = 12
    print "Difficulty  1 = easy, 2 = normal, 3 = hard"
    print "A is 6*6, B is 9*9, C is 12*12"
    print "Choice option example: option_a1"
    while True:
        a = str(raw_input("Which board do you want to play?: "))
        if a == "a1" or a == "a2" or a == "a3" or a == "b1" or a == "b2" or a == "b3" or a == "c":
            if a == "a1":
                i = a1
                j = a1
            if a == "a2":
                i = a2
                j = a2
            if a == "a3":
                i = a3
                j = a3
            if a == "b1":
                i = b1
                j = b1
            if a == "b2":
                i = b2
                j = b2
            if a == "b3":
                i = b3
                j = b3
            if a == "c":
                i = c
                j = c
            break
    Board(i, a)

start_rushhour()