CAR_ID = {'A': 'cyam2', 'B': 'CadetBlue', 'C': 'RoyalBlue1',
          'D': 'dark orange', 'T': 'red2'}

TRUCKS_ID = {'E': 'MediumPurple1', 'F': 'yellow2', 'Fa': 'yellow2',
             'G': 'gold', 'H': 'orange', 'I': 'gray64'}

# vehicle: id, x, y, orientation, i

class vehicle(object):
    def __init__(self, id, x, y, orientation, i):
        """ check is car if exists and assigns id, length and color"""
        self.i = i
        if id[0] in CAR_ID:
            self.id = id
            self.length = 2
        elif id[0] in TRUCKS_ID:
            self.id = id
            self.length = 3
        else:
            raise ValueError('Invalid id')


    #    """ check if x and y coordinates are legal, if yes assign them """

        if 0 <= x <= i:
            self.x = x
        else:
            raise ValueError('Invalid x')

        if 0 <= y <= i:
            self.y = y
        else:
            raise ValueError('Invalid y')


    #   """ check if orientation is correct, and if vehicle is outside board"""

        if orientation == 'hor':
            self.orientation = orientation
            x_end = self.x 
            y_end = self.y + (self.length - 1)
        elif orientation == 'ver':
            self.orientation = orientation
            x_end = self.x + (self.length - 1)
            y_end = self.y 
        else:
            raise ValueError('Invalid orientation {0}'.format(orientation))

        if x_end > self.i or y_end > self.i:
            raise ValueError('Invalid placing on board')


        print "Vehicle is oke!"