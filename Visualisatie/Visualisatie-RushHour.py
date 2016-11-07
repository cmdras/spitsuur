import Tkinter
from vehicle import vehicle

CAR_ID = {'A': 'green', 'B': 'CadetBlue', 'C': 'RoyalBlue1',
          'D': 'dark orange', 'T': 'red2', ' ': 'grey'}

TRUCKS_ID = {'E': 'MediumPurple1', 'F': 'yellow2', 'Fa': 'yellow2',
             'G': 'gold', 'H': 'orange', 'I': 'gray64'}


class Board(Tkinter.Frame):
    def __init__(self, width):
        self.width = width
        self.height = width
        vehicles = []
        with open('a1.txt', 'r') as f:
            for line in f:
                line = line[:-1] if line.endswith('\n') else line
                id, x, y, orientation = line
                print a
                vehicles.append(vehicle(id, int(x), int(y), orientation, 6))

        f.close()
        table = table_retriever(vehicles)
        # format of informationboard
        visualize(table, self.width, self.height)
        # prints the informationboard


def table_retriever(vehicles):
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
                table[y][x] = vehicle.id
                table[y][x+1] = vehicle.id
        else:
            for i in range(vehicle.length):
                table[y][x] = vehicle.id
                table[y+1][x] = vehicle.id
    return table


def visualize(table, width, height):
    canvas = Tkinter.Tk()
    for r in range(width):
        for c in range(height):
            Tkinter.Label(canvas, text=(table[r][c]), borderwidth=20, background=CAR_ID[table[r][c]]).grid(row=r, column=c)
    canvas.mainloop()

def start_rushhour():
    a1 = 6
    a2 = 6
    a3 = 6
    b = 9
    c = 12
    print "Difficulty  1 = easy, 2 = normal, 3 = hard"
    print "A is 6*6, B is 9*9, C is 12*12"
    print "Choice option example: option_a1"
    while True:
        a = str(raw_input("Which board do you want to play?: "))
        if a == "a1" or a == "a2" or a == "a3" or a == "b" or a == "c":
            if a == "a1":
                i = a1
                j = a1
            if a == "a2":
                i = a2
                j = a2
            if a == "a3":
                i = a3
                j = a3
            if a == "b":
                i = b
                j = b
            if a == "c":
                i = c
                j = c
            break
    Board(i)

start_rushhour()