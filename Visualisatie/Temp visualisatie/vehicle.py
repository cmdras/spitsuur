CAR_ID ={'A' : cyam2, 'B' : CadetBlue,
'C' : RoyalBlue1, 'D' : dark orange, 'T' : red2}

TRUCKS_ID ={'E' : MediumPurple1, 'F' : yellow2, 'Fa' : yellow2,
'G' : gold, 'H' : orange, 'I' : gray64}

vehicle: id, x, y, orientation, i

class vehicle(object):

    def __init__(self, id, x, y, orientation, i)

    """ check is car id exists and assigns id, length and color"""

    if id in CAR_ID:
        self.id = id
        self.length = 2
        self.color = CAR_ID.get('CAR_ID')

    elif id in TRUCK_ID:
        self.id = id
        self.length = 3
        self.color = TRUCKS_ID.get('TRUCKS_ID')

    else:
        raise ValueError('Invalid id')


    """ check if x and y coordinates are legal, if yes assign them """

    if 0 <= x <= i:
        self.x = x
    else:
        raise ValueError('Invalid x')

    if 0 <= y <= i:
        self.y = y
    else:
        raise ValueError('Invalid y')


    """ check if orientation is correct, and if vehicle is outside board"""

    if orientation == 'hor':
        self.orientation = orientation
        x_end = self.x + (self.length - 1)
        y_end = self.y
    elif orientation == 'ver':
        self.orientation = orientation
        x_end = self.x
        y_end = self.y + (self.length - 1)
    else:
        raise ValueError('Invalid orientation {0}'.format(orientation))

    if x_end > i or y_end > i:
        raise ValueError('Invalid placing on board')


    print "Vehicle is oke!"
    
