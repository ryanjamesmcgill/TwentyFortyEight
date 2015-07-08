"""
Clone of 2048 game.
Ryan McGill
2015
"""
import random
#import poc_2048_gui

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def  merge(line):
    """
    Merge function for 2048 game, 
    Takes input LIST and returns a new merged LIST.
    Always merges toward index 0.
    """
    match = 0
    seek = 1
    mline = line[:]

    while(seek < len(mline)):
        if(mline[seek] != 0):
            if (mline[match] == 0): #checking if seek just needs to be shifted towards index 0
                mline[match] = mline[seek]
                mline[seek] = 0
                seek = match
            else:
                if(mline[seek] == mline[match]): #checking if items need to be merged
                    mline[match] *= 2
                    mline[seek] = 0
                    match += 1
                    seek = match
                else:
                    if(match+1 != seek): #checking if seek is directly after match
                        mline[match+1]=mline[seek]
                        mline[seek]=0
                    match += 1
                    seek = match
        seek += 1
    return mline



class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._height = grid_height
        self._width = grid_width
        self.reset()
        self._initial = { 
                        UP: self.get_row_coordinates((0,0),OFFSETS[LEFT]),
                        LEFT: self.get_row_coordinates((0,0),OFFSETS[UP]),
                        DOWN: self.get_row_coordinates((self._height-1,0),OFFSETS[LEFT]),
                        RIGHT: self.get_row_coordinates((0,self._width-1),OFFSETS[UP])
                        }

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._board = [[0 for dummy_col in range(self._height)] for dummy_row in range(self._width)]
        #self.set_tile(1,0,20)
        #self.set_tile(4,1,1234)
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        spacing = 6
        str_board = ''
        for row in range(self._height):
            str_row=''
            for dummy_i in range(self._width): 
                str_row += '      '
            for col in range(self._width):
                if( len(str(self.get_tile(row,col))) >= spacing):
                    print "board value too large to print, increase spacing in ___str___ of TwentyFortyEight class!"
                    quit() #error checking
                str_row = self.insert_number(str_row, col*spacing, self.get_tile(row,col))
            str_board += str_row + '\n'
        return str_board

    def insert_number(self, string, position, number):
        """
        Inserts a value of @number into a string at index @position
        Used in TwentyFortyEight __str___ class
        """
        return string[:position] + str(number) + string[position:-len(str(number))]

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        tiles_changed = False

        for coordinate in self._initial[direction]:
            values = self.get_row_values(coordinate, OFFSETS[direction])
            if (values != merge(values)): 
                tiles_changed = True
            values = merge(values)
            self.put_row_values(coordinate, OFFSETS[direction], values)
        
        if( tiles_changed ):
            self.new_tile()


    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.

        returns True if a tile was placed in an empty tile
        returns False if there were no empty tiles available
        """
        # replace with your code
        zeros = []
        if(random.randint(1,10) > 9): 
            value = 4
        else: value = 2

        #create list of tiles containing zero
        for col in range(self._width):
            for row in range(self._height):
                if(self.get_tile(row,col) == 0): 
                    zeros.append([row,col])

        if(len(zeros) > 0): #check if any empty tiles remain in board
            coordinate = zeros[random.randint(0,len(zeros)-1)]
            row = coordinate[0]
            col = coordinate[1]
            self.set_tile(row,col,value)
            return True
        else:
            return False

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        Return False if coordinate is out of board range
        """
        if (len(self._board) <= col or len(self._board[0]) <= row):
            return False
        else:
            self._board[col][row] = value        

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        Return 'empty' if out of range
        """
        # check if coordinate is on grid
        if ( len(self._board) <= col or 
            len(self._board[0]) <= row or 
            col < 0 or 
            row < 0 ):
            return 'empty'
        else:
            return self._board[col][row]

    def get_row_coordinates(self, start, direction):
        """
        @start - Takes 1 starting coordinate
        @direction - direction row will itterate until end of grid is reached
        Returns list of coordinates itterating thru grid
        """
        coordinates = []
        coordinates.append(start)
        while(self.get_tile(coordinates[-1][0] + direction[0],coordinates[-1][1] + direction[1]) != 'empty'):
            new_coordinate = (coordinates[-1][0] + direction[0], coordinates[-1][1] + direction[1])
            coordinates.append(new_coordinate)
        return coordinates

    def get_row_values(self, start, direction):
        """
        @start - Takes 1 starting coordinate
        @direction - direction row will itterate until end of grid is reached
        Returns list of values itterating thru grid
        """
        values = []
        coordinates = self.get_row_coordinates(start, direction)
        for coordinate in coordinates:
            values.append(self.get_tile(coordinate[0], coordinate[1]))
        return values

    def put_row_values(self, start, direction, values):
        """
        Method for replacing a grid row or column with a list of values provided
        ** length of coordinates list and values list must be equal length, otherwise this function will print an error message
        @start - Takes 1 starting coordinate
        @direction - direction row will itterate until end of grid is reached
        @values - a list containing the values you want to be put in grid
        """
        coordinates = self.get_row_coordinates(start, direction)
        index = 0
        if(len(coordinates) != len(values)):
            print "error: TwentyFortyEight.put_row_values() was called but values and coordinates arrays were different lengths!"
        else:
            for coordinate in coordinates:
                self.set_tile(coordinate[0],coordinate[1],values[index])
                index += 1



#poc_2048_gui.run_gui(TwentyFortyEight(5, 2))
