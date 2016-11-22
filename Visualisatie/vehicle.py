CAR_ID = {'A': 'cyan2', 'B': 'CadetBlue', 'C': 'RoyalBlue1',
          'D': 'dark orange', 'T': 'red2'}

TRUCKS_ID = {'E': 'MediumPurple1', 'F': 'yellow2', 'Fa': 'yellow2',
             'G': 'gold', 'H': 'orange', 'I': 'gray64'}

# vehicle: id, x, y, orientation, i

class vehicle(object):
    def __init__(self, id, row_v, col_v, orientation, board_size):
        """ check is car if exists and assigns id, length and color"""
        self.board_size = board_size
        if id[0] in CAR_ID:
            self.id = id
            self.length = 2
        elif id[0] in TRUCKS_ID:
            self.id = id
            self.length = 3
        else:
            raise ValueError('Invalid id')


    #    """ check if x and y coordinates are legal, if yes assign them """

        if 0 <= row_v <= board_size:
            self.row_v = row_v
        else:
            raise ValueError('Invalid x')

        if 0 <= col_v <= board_size:
            self.col_v = col_v
        else:
            raise ValueError('Invalid y')


    #   """ check if orientation is correct, and if vehicle is outside board"""

        if orientation == 'hor':
            self.orientation = orientation
            row_v_end = self.row_v 
            col_v_end = self.col_v + (self.length - 1)
        elif orientation == 'ver':
            self.orientation = orientation
            row_v_end = self.row_v + (self.length - 1)
            col_v_end = self.col_v 
        else:
            raise ValueError('Invalid orientation {0}'.format(orientation))

        if row_v_end > self.board_size or col_v_end > self.board_size:
            raise ValueError('Invalid placing on board')


        print "Vehicle is oke!"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
