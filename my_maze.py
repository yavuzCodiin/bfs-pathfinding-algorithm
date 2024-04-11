import copy, random, types
from enum import Enum

class CellType(Enum):
    Empty = 1
    Block = 2

class CellMark(Enum):
    No = 0
    Start = 1
    End = 2

class Cell:
    def __init__(self, type = CellType.Empty, pos = None):
        self.type = type
        self.pos = pos
        self.count = 0
        self.path_from = None
        self.mark = CellMark.No

class Cell_Network:
    def __init__(self, board):
        self.board = board
    
    def get_size(self):
        """

        Get the size of the board. This method returns the dimensions of the board as a list, where the first element is the number of rows (height) and the second element is the number of columns (width).

        Parameters:
        ----------
        self : object
            The instance of the class from which this method is called. It must have a `board` attribute, which is a list of lists representing the grid.

        Returns:
        -------
        list of int
            A list containing two integers:
            - The first integer represents the number of rows(height) in the board.
            - The second integer represents the number of columns(width) in the board.

        """
        return [len(self.board), len(self.board[0])]
    
    def at(self, pos):
        """

        Retrieve the cell object at a specified position in the board.

        Parameters:
        ----------
        self : object
            The instance of the class from which this method is called.
        
        pos : list or tuple of int
            A list or tuple containing the [row_index, column_index] of the cell.

        Returns:
        -------
        Cell
          The cell object located at the specified position.

        """
        return self.board[pos[0]][pos[1]]
    
    def clone(self):
        """
        Clone the board.
        
        Parameters:
        ----------
        self : object
            The instance of the class from which this method is called.

        Returns:
        -------
        Cell_Network
          A copy of the board.

        """
        return Cell_Network(copy.deepcopy(self.board))
    
    def clear_count(self, count):
        """

        Clear the count of each cell

        Parameters:
        -----------
          self (object):
            The instance of the class from which this method is called.

          count (int): The number we want to give all the cell count.
        
        Returns:
        --------
          None  
        
        """
        for o in self.board:
            for i in o:
                i.count = count
                i.path_from = None

    def is_valid_point(self, pos):
        """

        Check if the given position is within the bounds of the board.
    
        Parameters:
        ----------
        self : object
            The instance of the class from which this method is called.
        
        pos : list or tuple of int
            A list or tuple containing the [row_index, column_index] of the cell.
    
        Returns:
        -------
        bool
          True if the position is within the bounds of the board, False otherwise.

        """
        sz = self.get_size()
        return (pos[0] >=0) and (pos[1] >= 0) and (pos[0] < sz[0]) and (pos[1] < sz[1])

def create_empty_maze(x, y): #create empty maze with board, start, end attributes
    """
    
    Create a empty maze and return its structure along with start and end points

    Parameters:
    ----------
    x (int):
        The width of the maze (number of cells horizontally).
 
    y (int):
        The height of the maze (number of cells vertically).

    Returns
    -------
    types.SimpleNamespace
        A namespace with the following attributes:
          - board : list of list of Cell objects
              The maze structure represented as a 2D grid.
          - start : list of int
              The starting coordinates [x, y] in the maze.
          - end : list of int
              The ending coordinates [x, y] in the maze.

    """
    return types.SimpleNamespace(
        board = Cell_Network( [[Cell(type=CellType.Empty, pos=[ix, iy]) for iy in range(y) ] for ix in range(x)] ),
        start=[random.randrange(0, x), random.randrange(0, y)],
        end= [random.randrange(0, x), random.randrange(0, y) ]
    )


def create_wall_maze(x, y):
    """

    Create a maze with walls and return its structure along with start and end points.

    Parameters:
    ----------
    x (int):
        The width of the maze (number of cells horizontally).
    y (int):
        The height of the maze (number of cells vertically).

    Returns:
    -------
    types.SimpleNamespace
        A namespace with the following attributes:
            - board : list of list of Cell objects
                The maze structure represented as a 2D grid.
            - start : list of int
                The starting coordinates [x, y] in the maze.
            - end : list of int
                The ending coordinates [x, y] in the maze.
    """
    #board creation
    board = [[Cell(type = CellType.Empty, pos=[ix,iy]) for iy in range(y)] for ix in range(x)]
    
    #wall creation
    for i in range(0,x):
        board[i][int(y/2)].type = CellType.Block
    for i in range(0,y):
        board[int(x/2)][i].type = CellType.Block

    #Wall Opening Creation    
    board[random.randint(0, x/2-1)][int(y/2)].type = CellType.Empty #random opening in the left half of the vertical wall
    board[random.randint(x/2+1, x-1)][int(y/2)].type = CellType.Empty #random opening in the right half of the vertical wall
    board[int(x/2)][random.randint(0, y/2-1)].type = CellType.Empty #random opening in the top half of the horizontal wall
    board[int(x/2)][random.randint(y/2+1, y-1)].type = CellType.Empty #random opening in the bottom half of the horizontal wall

    return types.SimpleNamespace( board = Cell_Network(board),
		start = [random.randrange(0,x/2), random.randrange(y/2+1,y)],
		end = [random.randrange(x/2+1,x), random.randrange(0,y/2)] )

def add_point(a, b):
    """
    
    Add two points represented by their coordinates.

    This function is typically used to calculate the position of neighboring cells by adding their relative positions to the current cell's position.

    Parameters:
    ----------
    a : list or tuple of int
        The [x, y] coordinates of the first point.
    b : list or tuple of int
        The [x, y] coordinates of the second point, often representing a relative position.

    Returns:
    -------
    list of int
        A list containing the resulting [x, y] coordinates after addition.
    
    """

    return [a[0]+ b[0], a[1]+ b[1]]